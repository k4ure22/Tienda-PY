import pymysql
pymysql.install_as_MySQLdb()

from django.db.backends.mysql.base import DatabaseWrapper

class PatchedDatabaseWrapper(DatabaseWrapper):
    def check_database_version_supported(self):
        # Saltamos la validación de versión de MariaDB
        return

import django.db.backends.mysql.base
django.db.backends.mysql.base.DatabaseWrapper = PatchedDatabaseWrapper
