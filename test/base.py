import sys

import mock
import pprint
from typing import Callable

import bryo.app.user
from suso.utils.context import LocalContext


def logger_debug(msg, *args, **kwargs):
    try:
        # stacks = inspect.stack()
        # stacks = [s for s in stacks if not s.filename.startswith("/home/winter.py")]
        # print(f" >>>> {stacks[-1].filename}")
        # print([s.filename for s in stacks])
        print(msg)
        # if args[-1]:
        #     print(args[-1])
    except:
        pass


class Tester:
    def __init__(self, email_or_user_id,
                 platform='ios',
                 code_name='emma',
                 app_version="11.0.0",
                 host_app_code_name='emma',
                 host_app_version="11.0.0",
                 rn_version='5.0.0',
                 locale='us'
                 ):
        if isinstance(email_or_user_id, int):
            self.user = bryo.app.user.get_user_by_id(email_or_user_id)
        else:
            self.user = bryo.app.user.fetch_user_by_email(email_or_user_id)
        assert self.user
        self.user_id = self.user['id']
        self.platform = platform
        self.code_name = code_name
        self.app_version = app_version
        self.host_app_code_name = host_app_code_name
        self.host_app_version = host_app_version
        self.rn_version = rn_version
        self.locale = locale

    def base_info(self):
        print(f"user_id {self.user_id}")

    rs_essential_columns = [
        "(TIMESTAMP 'epoch' + ts * INTERVAL '1 second') AS time",
        "event_name",

        "session_id",
        "session_name",

        "_subject_user_id",

        "_context_flavor",
        "_context_app",
        "_context_app_version",

        "_context_os",
        "_context_os_version",

        "_context_device_id",
        "_context_raw_device_id",

        "_context_locale",
        "_context_ip_address",
        "_context_lat",
        "_context_long",
        "_context_time_zone",
    ]

    def rs_query(self, sql):
        import mario.rs_base
        with mario.rs_base.psycopg2.connect(mario.rs_base.DSN) as conn:
            result = mario.rs_base.rs_query(conn, sql, return_dicts=True)
            return result

    def generate_sql(self, extra_columns=None, limit=None):
        if extra_columns:
            columns = self.rs_essential_columns + extra_columns
        else:
            columns = self.rs_essential_columns
        column_str = ",\n".join(columns)

        sql = f"""SELECT
{column_str}
 FROM unilogs_views_current_month uvcm
 WHERE _subject_user_id={self.user_id} 
 ORDER BY time desc"""
        if limit:
            sql += f" LIMIT {limit}"
        sql += ";"
        print(sql)

        print()
        # result = self.rs_query(sql)
        # pprint.pprint(result)
        # return sql

    def change_pwd(self, pwd):
        return bryo.app.user.update_user(self.user['id'], {'password': pwd})

    def extend_premium_secs(self, seconds):
        import bryo.app.iap
        return bryo.app.iap.extend_plan(self.user['id'], 'premium', int(seconds))

    def delete_user(self):
        return bryo.app.user.remove(self.user_id, False)

    def turn_off_mfa(self):
        import bryo.app.mfa
        bryo.app.mfa.remove_mfa(self.user_id, mfa_type=bryo.data.dbval.MFA.TYPE_SMS)

    def run(self, func_name, *args, **kwargs):
        with LocalContext(dict(
                code_name=self.code_name,
                platform=self.platform,
                app_version=self.app_version,
                host_app_code_name=self.host_app_code_name,
                host_app_version=self.host_app_version,
                rn_version=self.rn_version,
                locale=self.locale,
        )):
            func = getattr(self, func_name)
            if func and isinstance(func, Callable):
                print("----------------------------")
                print(f"=> {func_name} args={args} kwargs={kwargs}")
                result = func(*args, **kwargs)
                print("============================")
                pprint.pprint(result)
            else:
                raise Exception(f"no func {func_name}")


def get_function_by_name(function_name):
    try:
        return locals()[function_name]
    except KeyError:
        try:
            return globals()[function_name]
        except KeyError:
            raise ValueError(f"Function '{function_name}' not found")


def main(tester: Tester = None):
    with mock.patch("logging.LoggerAdapter.debug",
                    side_effect=logger_debug):
        input_args = sys.argv
        num_of_input_args = len(input_args)
        if num_of_input_args >= 2:
            func_name = input_args[1]
            func_args = input_args[2:] if num_of_input_args > 2 else []
            if tester:
                print(f"=> try run {func_name} in tester")
                tester.run(func_name, *func_args)
            else:
                print(f"=> try run {func_name} ")
                func = get_function_by_name(func_name)
                if func and isinstance(func, Callable):
                    func(*func_args)