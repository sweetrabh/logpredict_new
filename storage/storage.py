import pymssql
import numpy as np


# noinspection PyBroadException
class db_store:
    servername = 'localhost'
    databasename = 'parsedlogs'
    connection = ''

    def __init__(self):
        self.createschema()
        self.seedkeywords()
        # self.test()

    def startconnection(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * from logfiles")
        except:
            self.connection = pymssql.connect(server=self.servername, database=self.databasename)

    def closeconnection(self):
        self.connection.close()

    def getcursor(self):
        try:
            return self.connection.cursor()
        except:
            print("No database connection opened")

    def createschema(self):
        logfile = """
        IF OBJECT_ID('logfiles', 'U') IS NULL
            CREATE TABLE logfiles (
                id INT IDENTITY(1,1),
                logtype VARCHAR(100),
                totallines int NOT NULL,
                PRIMARY KEY(id)
        )
        """
        executions = """
            IF OBJECT_ID('executions', 'U') IS NULL
                CREATE TABLE executions(
                    id INT IDENTITY(1,1),
                    logfile_id int NOT NULL,
                    startline int NOT NULL,
                    endline int NOT NULL,
                    starttime VARCHAR(100),
                    endtime VARCHAR(100),
            )
            """
        logitems = """
            IF OBJECT_ID('logitems', 'U') IS NULL
                CREATE TABLE logitems(
                    id INT IDENTITY(1,1),
                    loglevel VARCHAR(200),
                    methodname VARCHAR(2000),
                    logmessage VARCHAR(MAX),
                    timestamp VARCHAR(100),
                    linenumber int NOT NULL,
                    execution_id int NOT NULL,
                    hasexception int NOT NULL,
            )
            """
        logexceptions = """
            IF OBJECT_ID('logexceptions', 'U') IS NULL
                CREATE TABLE logexceptions(
                    id INT IDENTITY(1,1),
                    methodname VARCHAR(2000),
                    description VARCHAR(MAX),
                    logitem_id int NOT NULL,
            )
            """
        stacktraces = """
            IF OBJECT_ID('stacktraces', 'U') IS NULL
                CREATE TABLE stacktraces(
                    id INT IDENTITY(1,1),
                    methodname VARCHAR(2000),
                    filename VARCHAR(2000),
                    linenumber int NOT NULL,
                    logexception_id int NOT NULL,
            )
            """
        seed_categories = """
            IF OBJECT_ID('seed_categories', 'U') IS NULL
                CREATE TABLE seed_categories(
                    id INT IDENTITY(1,1),
                    keyword VARCHAR(2000),
                    PRIMARY KEY(keyword),

            )
            """
        seed_words = """
            IF OBJECT_ID('seed_words', 'U') IS NULL
                CREATE TABLE seed_words(
                    id INT IDENTITY(1,1),
                    keyword VARCHAR(2000),
                    category_id INT NULL,
                    PRIMARY KEY(keyword),

            )
            """
        dictionary_words = """
            IF OBJECT_ID('dictionary_words', 'U') IS NULL
                CREATE TABLE dictionary_words(
                    id INT IDENTITY(1,1),
                    keyword VARCHAR(2000),
                    PRIMARY KEY(keyword),
            )
            """
        lf_features = """
            IF OBJECT_ID('lf_features', 'U') IS NULL
                CREATE TABLE lf_features(
                    id INT IDENTITY(1,1),
                    log_id int not NULL,
                    f0 int NOT NULL,
                    f1 int NOT NULL,
                    f2 int NOT NULL,
                    f3 int NOT NULL,
                    f4 int NOT NULL,
                    f5 int NOT NULL,
                    f6 int NOT NULL,
                    f7 int NOT NULL,
                    f8 int NOT NULL,
                    f9 int NOT NULL,
                    f10 int NOT NULL,
                    f11 int NOT NULL,
                    f12 int NOT NULL,
                    f13 int NOT NULL,
                    f14 int NOT NULL,
                    f15 int NOT NULL,
                    f16 int NOT NULL,
                    f17 int NOT NULL,
                    f18 int NOT NULL,
                    f19 int NOT NULL,
                    f20 int NOT NULL,
                    f21 int NOT NULL,
                    f22 int NOT NULL,
                    f23 int NOT NULL,
                    f24 int NOT NULL,
                    f25 int NOT NULL,
                    f26 int NOT NULL,
                    f27 int NOT NULL,
                    f28 int NOT NULL,
                    f29 int NOT NULL,
                    f30 int NOT NULL,
                    f31 int NOT NULL,
                    f32 int NOT NULL,
                    f33 int NOT NULL,
                    f34 int NOT NULL,
                    f35 int NOT NULL,
                    f36 int NOT NULL,
                    f37 int NOT NULL,
                    f38 int NOT NULL,
                    f39 int NOT NULL,
                    PRIMARY KEY(log_id),
            )
            """

        self.startconnection()
        cs = self.connection.cursor()

        cs.execute(logfile)
        cs.execute(executions)
        cs.execute(logitems)
        cs.execute(logexceptions)
        cs.execute(stacktraces)
        cs.execute(seed_words)
        cs.execute(seed_categories)
        cs.execute(dictionary_words)
        cs.execute(lf_features)
        self.connection.commit()
        self.closeconnection()
        print("Schema created")

    def seedkeywords(self):
        categories_dict = {}
        seed_words = ['sca', 'debug', '-logfile', 'systemspec', 'args', 'server', 'scan', '.fpr',
                      '.fmdalgeneralexception',
                      'operatingsystemmxbean', '.hibernate', '.escalatinglog4jreceiver', 'show -runtime',
                      'com.fortify.manager.service.emailserviceimpl',
                      'tomcat', 'ldap validation', 'master info', 'master fine', 'master warning', '.nst', 'tomcat',
                      'catalina', 'MysqlParameterMetadata',
                      'com.mysql.jdbc.SQLError.createSQLException',
                      "memory", "GC", "resources", "MaxPermSize", 'packet', 'packet sent', 'received any packets',
                      'FortifyException', 'ConnectException', 'Connection', 'timed', 'connect',
                      'java.net.DualStackPlainSocketImpl.connect0(Native Method)', 'Connection timed out', 'accessible',
                      'not accessible',
                      'not down', 'overloaded', 'Connection refused', 'RulepackBLLImpl',
                      'com.fortify.manager.BLL.impl.RulepackBLLImpl', 'importinstalledrulepacks',
                      'Exception importinstalledrulepacks',
                      'FortifyException', 'security content', 'certpath', 'sun.security.validator.ValidatorException',
                      'ValidatorException', 'PKIX', 'BugTrackerException',
                      'com.fortify.pub.bugtracker.support.BugTrackerException', 'SSLHandshakeException',
                      'SunCertPathBuilderException', 'certification', 'valid certification path', 'PKIXValidator',
                      'HY000',
                      '.SqlExceptionHelper', 'SQL Error', 'seeding', 'Migration', 'assertion', 'Hibernate',
                      'com.microsoft.sqlserver.jdbc.SQLServerException', 'SQLServerException',
                      'org.hibernate.exception.constraintviolationexceptioncould', 'hibernatedatabaseinterface.java',
                      'sqlexceptionhelper.java', 'database', 'hibernate', 'DB2', 'mysql', 'SQLException',
                      'com.fortify.manager.service.scheduler.SchedulerManagerImpl',
                      'org.hibernate.engine.jdbc.spi.SqlExceptionHelper', 'transaction', 'JDBCConnectionException',
                      'SQLState', 'RuntimeControllerConnectionConfiguration',
                      'Initializing runtime', 'event handlers',
                      'Initializing runtime event handlers', '10234',
                      'com.fortify.manager.service.runtime.RuntimeControllerConnectionConfiguration', 'certification',
                      'unable to find valid certification path to requested target',
                      'sun.security.provider.certpath.SunCertPathBuilderException',
                      'sun.security.provider.certpath.SunCertPathBuilderException',
                      'sun.security.validator.ValidatorException',
                      'org.apache.xmlrpc.XmlRpcException', 'javax.net.ssl.SSLHandshakeException',
                      'java.security.cert.CertificateException', 'Bugzilla',
                      'com.fortify.pub.bugtracker.support.BugTrackerAuthenticationException',
                      'com.fortify.pub.bugtracker.support.BugTrackerAuthenticationException',
                      'Bugzilla4BugTrackerPlugin',
                      'ScanProcessAuthorizationException', 'authorization', 'REQUIRE_AUTHORIZATION', 'upload artifact',
                      'ArtifactUploadJob', 'SessionTimeoutFilter', 'upload', 'port', '10234', 'UserError',
                      'com.fortify.manager.service.parser.checker.ScanProcessAuthorizationException', 'Authentication',
                      'AuthenticationSuccessEvent', 'Authentication event AuthenticationSuccessEvent: admin',
                      'org.eclipse.birt.report.engine.api.impl.reportengine',
                      'org.eclipse.birt.report.engine.layout.html',
                      'org.eclipse.birt.data.engine.odaconsumer', 'parameter', 'birt', 'ReportBLLImpl', 'report',
                      'report generation', 'jobCallback', 'Trigger', 'PV$', 'scheduler', 'Quartz',
                      'com.fortify.manager.BLL.jobs.cron.RecurringLdapRefreshJob', 'job scheduler', 'job recovery',
                      'NameNotFoundException', 'ldap', 'DirectLdapObjectSource',
                      'com.fortify.manager.service.ldap.impl.DirectLdapObjectSource',
                      'javax.naming.CommunicationException', 'simple bind', 'severe', 'fatal', 'bind',
                      'convertLdapException', 'LdapClient', 'sun.security.ssl', 'sun.security.provider', 'SQLCODE',
                      'DB2',
                      'DB', 'SQLRecoverableException',
                      'Upload artifact', 'artifact failed', 'quartz', 'com.microsoft.sqlserver', 'bad SQL', 'appserver',
                      'database', 'ldap', 'quartz', 'ssl', 'critical', 'tomcat', 'jboss', 'catalina', 'servlet',
                      'quartz', 'scheduler', 'Error', 'unable', 'fail', 'exception', 'failed', 'invalid', 'error',
                      'Intercepted',
                      'nested exception', 'transaction', 'Hibernate', 'column', 'SQL', 'Communications link',
                      'artifact', 'SQLState', 'LDAP', 'com.fortify.manager.DAO.UsernameAndEmail', 'LDAP object', 'PKIX',
                      'valid certification', 'sun.security.provider.certpath.SunCertPathBuilderException:',
                      'simple bind', 'javax.net.ssl.SSLHandshakeException']

        appserver_words = ['tomcat', 'jboss', 'catalina', 'servlet']
        quartz_words = ['quartz', 'scheduler']
        critical_words = ['Error', 'unable', 'fail', 'exception', 'failed', 'invalid', 'error', 'Intercepted',
                          'nested exception']
        database_words = ['transaction', 'Hibernate', 'column', 'SQL', 'Communications link', 'artifact', 'SQLState']
        ldap_words = ['LDAP', 'com.fortify.manager.DAO.UsernameAndEmail', 'LDAP object']
        ssl_words = ['PKIX', 'valid certification', 'sun.security.provider.certpath.SunCertPathBuilderException:',
                     'simple bind', 'javax.net.ssl.SSLHandshakeException', ]

        li_categories = ['appserver', 'quartz', 'critical', 'database', 'ldap', 'ssl']

        self.startconnection()
        curs = self.connection.cursor()

        # Write the list of categories to the database
        for category in li_categories:
            try:
                curs.execute(
                    "INSERT INTO seed_categories VALUES(%s)", category
                )
                categories_dict[category] = curs.lastrowid
            except:
                pass

        # Write logitem categories to li_categories, write their corresponding keywords to li_seed
        for word in seed_words:
            cat_id = 0
            try:
                if word in appserver_words:
                    cat_id = categories_dict['appserver']
                if word in quartz_words:
                    cat_id = categories_dict['quartz']
                if word in critical_words:
                    cat_id = categories_dict['critical']
                if word in database_words:
                    cat_id = categories_dict['database']
                if word in ldap_words:
                    cat_id = categories_dict['ldap']
                if word in ssl_words:
                    cat_id = categories_dict['ssl']

                curs.execute(
                    "INSERT INTO seed_words VALUES(%s, %d)",
                    (word, cat_id)
                )
            except Exception as e:
                # print(word, e)
                pass

        self.connection.commit()
        self.closeconnection()

    def write_logfile(self, logfile):
        self.startconnection()
        lfcursor = self.connection.cursor()
        lfcursor.execute("INSERT INTO logfiles VALUES(%d, %s)", (logfile.scantype, logfile.totallines))
        lf_id = lfcursor.lastrowid
        self.connection.commit()
        self.closeconnection()
        return lf_id

    def write_execution(self, execution, lf_id, execcursor=False):
        if execcursor is False:
            self.startconnection()
            execcursor = self.connection.cursor()
        execcursor.execute("INSERT INTO executions VALUES(%d, %d, %d, %s, %s)", (
            lf_id, execution.startline, execution.endline, str(execution.starttime), str(execution.endtime)))
        exec_id = execcursor.lastrowid
        self.connection.commit()
        return exec_id

    def write_logitem(self, logitem, exec_id, licursor=False):
        if licursor is False:
            self.startconnection()
            licursor = self.connection.cursor()

        # Get value for hasException column
        if logitem.hasExceptions():
            hasexception = 1
        else:
            hasexception = 0

        try:
            # Write logitem to the database
            licursor.execute("INSERT INTO logitems VALUES(%s, %s, %s, %s, %d, %d, %d)", (
                logitem.loglevel, str(logitem.methodname), str(logitem.logmessage), str(logitem.datetimestamp),
                logitem.linenumber,
                exec_id, hasexception))

            li_id = licursor.lastrowid

            # Check if the logitem has exceptions, write those to the database as well
            if logitem.hasExceptions():
                exceptions = logitem.getExceptions()
                for exception in exceptions:
                    licursor.execute("INSERT INTO logexceptions VALUES(%s, %s, %d)",
                                     (exception.methodname, exception.description, li_id))
                    le_id = licursor.lastrowid

                    # Check if the current exception has a stacktrace, write those to the database as well
                    if exception.stacktrace.__len__() > 0:
                        stacktraces = exception.stacktrace
                        for st in stacktraces:
                            licursor.execute("INSERT INTO stacktraces VALUES(%s, %s, %d, %d)",
                                             (st.method, st.filename, st.linenumber, le_id))

            self.connection.commit()
            return li_id

        except Exception as e:
            print(e)
            print(logitem.loglevel, logitem.methodname, logitem.logmessage)
            return -1

    def write_logitems(self, logitems, exec_id):
        self.startconnection()
        licursor = self.connection.cursor()
        li_id = []
        for logitem in logitems:
            li_id.append(self.write_logitem(logitem, exec_id, licursor=licursor))
        self.closeconnection()
        return li_id

    def getdictionarykeywordsbyid(self, keywords):
        self.startconnection()
        csk = self.connection.cursor()
        kwids = []
        for keyword in keywords:
            selecctt = "select id from dictionary_words where keyword='%s'" % keyword
            csk.execute(selecctt)
            kwid = csk.fetchone()
            try:
                kwids.append(kwid[0])
            except:
                kwids.append(-1)
        self.closeconnection()
        return kwids

    def writeLFfeatures(self, kwids, lfid):
        self.startconnection()
        kwc = self.connection.cursor()
        try:
            kwc.execute(
                "INSERT INTO lf_features VALUES(%d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d,"
                " %d, %d)",
                (lfid, kwids[0], kwids[1], kwids[2], kwids[3], kwids[4], kwids[5], kwids[6], kwids[7], kwids[8],
                 kwids[9], kwids[10], kwids[11], kwids[12], kwids[13], kwids[14], kwids[15], kwids[16], kwids[17],
                 kwids[18], kwids[19], kwids[20], kwids[21], kwids[22], kwids[23], kwids[24], kwids[25], kwids[26],
                 kwids[27], kwids[28], kwids[29], kwids[30], kwids[31], kwids[32], kwids[33], kwids[34], kwids[35],
                 kwids[36], kwids[37], kwids[38], kwids[39]))
            self.connection.commit()
            self.closeconnection()
        except:
            self.closeconnection()

    def getLFfeatures(self):
        self.startconnection()
        ctx = self.connection.cursor()

        selectstf = "SELECT * FROM lf_features INNER JOIN logfiles ON lf_features.log_id=logfiles.id"
        ctx.execute(selectstf)
        data = np.asarray(ctx.fetchall())

        # Logfile features
        features = np.asarray(data[:, 2:42]).astype(dtype=int)

        # Target outputs
        logtypes_raw = data[:, 43]
        logtypes_target = []
        for ltr in logtypes_raw:
            if ltr == 'dsca':
                logtypes_target.append(1)
            elif ltr == 'sca':
                logtypes_target.append(2)
            elif ltr == 'ssc':
                logtypes_target.append(3)
            else:
                print("No targets exist")

        return features, logtypes_target

    def test(self):
        selectst = 'SELECT * from logfiles where id=250'

        self.startconnection()

        c2 = self.connection.cursor()
        c2.execute(selectst)
        results = c2.fetchall()

        selectexec = 'SELECT * from exec_seed'
        c2.execute(selectexec)
        executions_keywords = np.asarray(c2.fetchall())
        num_results = executions_keywords.__len__()
        print("\nFrom exec_seed keywords: %d words" % num_results)
        words = executions_keywords[:, 1]
        for exece in words:
            print(exece)

# dbwriter = db_store()
# dbwriter.test()