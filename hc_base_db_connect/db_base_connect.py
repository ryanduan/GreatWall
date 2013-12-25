# coding=utf-8
import threading
import copy
import logging
from DBUtils.PersistentDB import PersistentDB
from DBUtils.SimplePooledDB import PooledDB
try:
    import MySQLdb
    import MySQLdb.constants
    import MySQLdb.converters
    import MySQLdb.cursors
except ImportError:
    # If MySQLdb isn't available this module won't actually be useable,
    # but we want it to at least be importable (mainly for readthedocs.org,
    # which has limitations on third-party modules)
    MySQLdb = None
from pymongo import MongoClient
import itertools
from MySQLdb import MySQLError
import redis

__author__ = 'Siglud'


def get_db_pool(host, user, passwd, db=None,
                use_unicode=True, charset='utf8',
                timezone="+8:00", autocommit=True,
                mincached=1, maxcached=20,
                maxshared=0, maxconnections=100, blocking=True,
                maxusage=None, setsession=None, reset=True,
                failures=None, ping=1):
    """
        creator: either an arbitrary function returning new DB-API 2
            connection objects or a DB-API 2 compliant database module
        mincached: initial number of idle connections in the pool
            (0 means no connections are made at startup)
        maxcached: maximum number of idle connections in the pool
            (0 or None means unlimited pool size)
        maxshared: maximum number of shared connections
            (0 or None means all connections are dedicated)
            When this maximum number is reached, connections are
            shared if they have been requested as shareable.
        maxconnections: maximum number of connections generally allowed
            (0 or None means an arbitrary number of connections)
        blocking: determines behavior when exceeding the maximum
            (if this is set to true, block and wait until the number of
            connections decreases, otherwise an error will be reported)
        maxusage: maximum number of reuses of a single connection
            (0 or None means unlimited reuse)
            When this maximum usage number of the connection is reached,
            the connection is automatically reset (closed and reopened).
        setsession: optional list of SQL commands that may serve to prepare
            the session, e.g. ["set datestyle to ...", "set time zone ..."]
        reset: how connections should be reset when returned to the pool
            (False or None to rollback transcations started with begin(),
            True to always issue a rollback for safety's sake)
        failures: an optional exception class or a tuple of exception classes
            for which the connection failover mechanism shall be applied,
            if the default (OperationalError, InternalError) is not adequate
        ping: determines when the connection should be checked with ping()
            (0 = None = never, 1 = default = whenever fetched from the pool,
            2 = when a cursor is created, 4 = when a query is executed,
            7 = always, and all other bit combinations of these values)
        """
    db_kwargs = dict(user=user, passwd=passwd, conv=CONVERSIONS, use_unicode=use_unicode, charset=charset)
    if db is not None:
        db_kwargs['db'] = db

    autocommit = 1 if autocommit else 0
    db_kwargs['init_command'] = 'SET time_zone = "%s";SET autocommit=%d' % (timezone, autocommit)

    host_pair = host.split(":")
    if len(host_pair) == 2:
        db_kwargs['host'] = host_pair[0]
        db_kwargs['port'] = int(host_pair[1])
    else:
        db_kwargs['host'] = host
        db_kwargs['port'] = 3306

    return PooledDB(creator=MySQLdb, mincached=mincached, maxcached=maxcached, maxshared=maxshared,
                    maxconnections=maxconnections,
                    blocking=blocking, maxusage=maxusage, setsession=setsession, reset=reset, failures=failures,
                    ping=ping,
                    **db_kwargs)


def get_db_persistent(host, user, passwd, db=None,
                      use_unicode=True, charset='utf8',
                      timezone="+8:00", autocommit=True,
                      maxusage=None, setsession=None, failures=None, ping=1,
                      closeable=False, threadlocal=None):
    """
        creator: either an arbitrary function returning new DB-API 2
            connection objects or a DB-API 2 compliant database module
        maxusage: maximum number of reuses of a single connection
            (number of database operations, 0 or None means unlimited)
            Whenever the limit is reached, the connection will be reset.
        setsession: optional list of SQL commands that may serve to prepare
            the session, e.g. ["set datestyle to ...", "set time zone ..."]
        failures: an optional exception class or a tuple of exception classes
            for which the connection failover mechanism shall be applied,
            if the default (OperationalError, InternalError) is not adequate
        ping: determines when the connection should be checked with ping()
            (0 = None = never, 1 = default = whenever it is requested,
            2 = when a cursor is created, 4 = when a query is executed,
            7 = always, and all other bit combinations of these values)
        closeable: if this is set to true, then closing connections will
            be allowed, but by default this will be silently ignored
        threadlocal: an optional class for representing thread-local data
            that will be used instead of our Python implementation
            (threading.local is faster, but cannot be used in all cases)
        args, kwargs: the parameters that shall be passed to the creator
            function or the connection constructor of the DB-API 2 module

        """
    db_kwargs = dict(user=user, passwd=passwd, conv=CONVERSIONS, use_unicode=use_unicode, charset=charset)
    if db is not None:
        db_kwargs['db'] = db

    autocommit = 1 if autocommit else 0
    db_kwargs['init_command'] = 'SET time_zone = "%s";SET autocommit=%d' % (timezone, autocommit)

    host_pair = host.split(":")
    if len(host_pair) == 2:
        db_kwargs['host'] = host_pair[0]
        db_kwargs['port'] = int(host_pair[1])
    else:
        db_kwargs['host'] = host
        db_kwargs['port'] = 3306

    return PersistentDB(creator=MySQLdb, maxusage=maxusage, setsession=setsession, failures=failures, ping=ping,
                        closeable=closeable, threadlocal=threadlocal,
                        **db_kwargs)


class MongoConnection(object):
    conn_dict = {}
    conn_lock = threading.Lock()

    @classmethod
    def get_conn(cls, host, port, dbname):
        with cls.conn_lock:
            if cls.conn_dict.get((host, port), None) is None:
                cls.conn_dict[(host, port)] = MongoClient(host, port)
            conn = cls.conn_dict[(host, port)]
        return conn[dbname]


class Connection(object):
    def __init__(self, db_pool, db_name=None):
        """
        传入连接池,生成连接
        """
        self._db_pool = db_pool
        self._conn = None
        #self._initialized=False
        self._retry = 2

        #args
        self._host = db_pool._kwargs.get('host', '')
        self._db = db_pool._kwargs.get('db', None)
        if self._db is None and db_name is None:
            raise AttributeError('db_name must not be None while pool initialized without db')
        if db_name is not None and type(db_name) is not str and type(db_name) is not unicode:
            raise TypeError('db_name must be str or unicode')
        self._db_name = db_name

        #try:
        #    self.reconnect()
        #except:
        #    logging.error("Initial connection error",
        #        exc_info=True)

    def __del__(self):
        self.close()

    def close(self):
        """Closes this database connection pool."""
        if getattr(self, "_conn", None) is not None:
            self._conn.close()
            self._conn = None

    def reconnect(self):
        """
        单连接重连机制
        """
        self.close()
        self._conn = self._db_pool.connection(False)
        if (self._db is None) and (self._db_name is not None):
            cur = self._conn.cursor()
            cur.execute('use %s' % self._db_name)
            cur.close()

    def _ensure_connected(self):
        #if self._initialized==False:
        #    self._db_pool.close()
        #    self.reconnect()
        #    self._initialized=True
        if getattr(self, "_conn", None) is not None:
            try:
                self._conn.ping()
            except OperationalError:
                self.reconnect()
        else:
            self.reconnect()

    def _cursor(self):
        self._ensure_connected()
        return self._conn.cursor()

    def _execute(self, cursor, query, parameters):
        try:
            return cursor.execute(query, parameters)
        #except OperationalError:
        except Exception as e:
            logging.error(e)
            self.close()
            raise

    def iter(self, query, *parameters):
        """SSCursor"""
        return

    def query(self, query, *parameters):
        """Returns a row list for the given query and parameters."""
        count = 0
        errorContent = None
        while count < self._retry:
            cursor = self._cursor()
            try:
                self._execute(cursor, query, parameters)
                self._conn.close()
                column_names = [d[0] for d in cursor.description]
                return [Row(itertools.izip(column_names, row)) for row in cursor]
            except Exception as e:
                logging.error(e)
                errorContent = e
                self.reconnect()
                count += 1
            finally:
                cursor.close()
        raise MySQLError(errorContent)

    def get(self, query, *parameters):
        """Returns the first row returned for the given query."""
        #basic method query
        rows = self.query(query, *parameters)
        if not rows:
            return None
        elif len(rows) > 1:
            raise MySQLError("Multiple rows returned for Database.get() query")
        else:
            return rows[0]

    def execute(self, query, *parameters):
        """Executes the given query, returning the lastrowid from the query."""
        #basic method execute_lastrowid
        return self.execute_lastrowid(query, *parameters)

    def execute_lastrowid(self, query, *parameters):
        """Executes the given query, returning the lastrowid from the query."""
        count = 0
        while count < self._retry:
            cursor = self._cursor()
            try:
                self._execute(cursor, query, parameters)
                self._conn.close()
                assert cursor.rowcount != -1
                return cursor.lastrowid
            except Exception as e:
                logging.error(e)
                self.reconnect()
                count += 1
            finally:
                cursor.close()
        raise MySQLError("failed 2 times in execute_lastrowid()")

    def execute_rowcount(self, query, *parameters):
        """Executes the given query, returning the rowcount from the query."""
        count = 0
        while count < self._retry:
            cursor = self._cursor()
            try:
                self._execute(cursor, query, parameters)
                self._conn.close()
                assert cursor.rowcount != -1
                return cursor.rowcount
            except Exception as e:
                logging.error(e)
                self.reconnect()
                count += 1
            finally:
                cursor.close()
        raise MySQLError("failed 2 times in execute_rowcount()")

    def executemany(self, query, parameters):
        """Executes the given query against all the given param sequences.

        We return the lastrowid from the query.
        """
        #basic method executemany_lastrowid
        return self.executemany_lastrowid(query, parameters)

    def executemany_lastrowid(self, query, parameters):
        """Executes the given query against all the given param sequences.

        We return the lastrowid from the query.
        """
        cursor = self._cursor()
        try:
            cursor.executemany(query, parameters)
            return cursor.lastrowid
        finally:
            cursor.close()

    def executemany_rowcount(self, query, parameters):
        """Executes the given query against all the given param sequences.

        We return the rowcount from the query.
        """
        cursor = self._cursor()
        try:
            cursor.executemany(query, parameters)
            return cursor.rowcount
        finally:
            cursor.close()


class Row(dict):
    """A dict that allows for object-like property access syntax."""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)


if MySQLdb is not None:
    # Fix the access conversions to properly recognize unicode/binary
    FIELD_TYPE = MySQLdb.constants.FIELD_TYPE
    FLAG = MySQLdb.constants.FLAG
    CONVERSIONS = copy.copy(MySQLdb.converters.conversions)

    field_types = [FIELD_TYPE.BLOB, FIELD_TYPE.STRING, FIELD_TYPE.VAR_STRING]
    if 'VARCHAR' in vars(FIELD_TYPE):
        field_types.append(FIELD_TYPE.VARCHAR)

    for field_type in field_types:
        CONVERSIONS[field_type] = [(FLAG.BINARY, str)] + CONVERSIONS[field_type]

    # Alias some common MySQL exceptions
    IntegrityError = MySQLdb.IntegrityError
    OperationalError = MySQLdb.OperationalError


class Dao(object):
    """数据库连接"""
    def __init__(self, ConfigSetting):
        """
        @type ConfigSetting: models.config.Config
        """
        self.configSetting = ConfigSetting
        #for pycharm auto completion only
        if False:
            self.mongo_customservice = None
            """:type: MongoClient"""
            self.mongo_admin = None
            """:type: MongoClient"""
            self.mongo_liveshow = None
            """:type: MongoClient"""
            self.mysql_basic_write = None
            """:type: Connection"""
            self.mysql_basic_read = None
            """:type: Connection"""
            self.mysql_admin_write = None
            """:type: Connection"""
            self.mysql_admin_read = None
            """:type: Connection"""
            self.mysql_virtual_write = None
            """:type: Connection"""
            self.mysql_virtual_read = None
            """:type: Connection"""
            self.mysql_rank_write = None
            """:type: Connection"""
            self.mysql_rank_read = None
            """:type: Connection"""
            self.login_write = redis.Redis()
            self.post_write = redis.Redis()
            self.pic_write = redis.Redis()
            self.comment_write = redis.Redis()
            self.tencent_write = redis.Redis()
            self.weibo_write = redis.Redis()
            self.fansGroup_write = redis.Redis()
            self.post_delete_write = redis.Redis()
            self.comment_delete_write = redis.Redis()
            self.session_write = redis.Redis()
            self.static_write = redis.Redis()
            self.profile_write = redis.Redis()
            self.room_info_write = redis.Redis()
            self.superFan_write = redis.Redis()
            self.user_info_write = redis.Redis()
            self.user_ext_write = redis.Redis()
            self.ol_user_write = redis.Redis()
            self.broadcast_write = redis.Redis()
            self.challenge_write = redis.Redis()
            self.emoticon_write = redis.Redis()
            self.events_write = redis.Redis()
            self.live_show_write = redis.Redis()
            self.tools_write = redis.Redis()
            self.padmin_write = redis.Redis()
            self.live_backend_write = redis.Redis()
            self.im_write = redis.Redis()
            self.virtual_write = redis.Redis()
            self.siteadmin_write = redis.Redis()
            self.cache_write = redis.Redis()
            self.siteEvent_write = redis.Redis()
            self.superfan_write = redis.Redis()
            self.music_write = redis.Redis()
            self.music_album_write = redis.Redis()
            self.fake_write = redis.Redis()
            self.feed_write = redis.Redis()
            self.system_notice_write = redis.Redis()
            self.htmlcache_write = redis.Redis()
            self.util_write = redis.Redis()
            self.tencent_olduser_write = redis.Redis()
            self.user_card_writ = redis.Redis()
            self.activity_write = redis.Redis()
            self.video_write = redis.Redis()
            self.index_write = redis.Redis()
            self.login_read = redis.Redis()
            self.post_read = redis.Redis()
            self.pic_read = redis.Redis()
            self.comment_read = redis.Redis()
            self.tencent_read = redis.Redis()
            self.weibo_read = redis.Redis()
            self.fansGroup_read = redis.Redis()
            self.post_delete_read = redis.Redis()
            self.comment_delete_read = redis.Redis()
            self.session_read = redis.Redis()
            self.static_read = redis.Redis()
            self.profile_read = redis.Redis()
            self.room_info_read = redis.Redis()
            self.superFan_read = redis.Redis()
            self.user_info_read = redis.Redis()
            self.user_ext_read = redis.Redis()
            self.ol_user_read = redis.Redis()
            self.broadcast_read = redis.Redis()
            self.challenge_read = redis.Redis()
            self.emoticon_read = redis.Redis()
            self.events_read = redis.Redis()
            self.live_show_read = redis.Redis()
            self.tools_read = redis.Redis()
            self.padmin_read = redis.Redis()
            self.live_backend_read = redis.Redis()
            self.im_read = redis.Redis()
            self.virtual_read = redis.Redis()
            self.siteadmin_read = redis.Redis()
            self.cache_read = redis.Redis()
            self.siteEvent_read = redis.Redis()
            self.superfan_read = redis.Redis()
            self.music_read = redis.Redis()
            self.music_album_read = redis.Redis()
            self.fake_read = redis.Redis()
            self.feed_read = redis.Redis()
            self.system_notice_read = redis.Redis()
            self.htmlcache_read = redis.Redis()
            self.util_read = redis.Redis()
            self.tencent_olduser_read = redis.Redis()
            self.user_card_writ = redis.Redis()
            self.activity_read = redis.Redis()
            self.video_read = redis.Redis()
            self.index_read = redis.Redis()

    def __getattr__(self, item):
        """获取数据库实例
        :rtype: Connection
        """
        if "write" in item or "read" in item or "mongo" in item:
            if hasattr(self, "_{}".format(item)):
                return getattr(self, "_{}".format(item))
            if "mongo" in item:
                connections = MongoConnection.get_conn(
                    getattr(self.configSetting, "%s_host" % item),
                    getattr(self.configSetting, "%s_port" % item),
                    getattr(self.configSetting, "%s_db" % item))
            elif "mysql" in item:
                connections = Connection(
                    get_db_persistent(
                        getattr(self.configSetting, "%s_host" % item),
                        getattr(self.configSetting, "%s_user" % item),
                        getattr(self.configSetting, "%s_password" % item),
                        db=getattr(self.configSetting, "%s_db" % item)))
            else:
                connections = redis.Redis(
                    connection_pool=redis.ConnectionPool(
                        host=getattr(self.configSetting, "%s_host" % item),
                        port=getattr(self.configSetting, "%s_port" % item),
                        db=getattr(self.configSetting, "%s_db" % item)))
            setattr(self, "_{}".format(item), connections)
            return connections
        raise AttributeError

    def __fakeFunction(self, other):
        return other.__doc__