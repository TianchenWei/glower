from base import *


class PremiumTester(Tester):
    def test_example(self):
        print("==> test_example")

    def test_premium(self):
        import bryo.app.ps_discount.base
        from bryo.app.ps_discount.staged_discount_op import read_granted_discount, StagedDiscountOp

        ctx = bryo.app.ps_discount.base.SaleCtx(
            self.user_id,
            self.platform,
            self.code_name,
            bryo.app.user.get,
            bryo.app.user.get_tz)
        op = StagedDiscountOp(ctx)
        for _op in op._ordered_ops:
            print(_op)
        op.peek_next()
        granted = read_granted_discount(self.user_id, self.code_name)
        print("==> granted")
        pprint.pprint(granted)

        discounts = bryo.app.discount.discounts_for_user(self.user_id, self.platform, self.code_name)
        print("==> discounts")
        pprint.pprint(discounts)

        print("==> fetch_plan_config_v3")
        result = bryo.app.iap.fetch_plan_config_v3(
            self.user_id,
            self.platform,
            self.code_name,
            '10.0.0')
        print('v3/pids', ([p['product_id'] for p in result['plans']]))
        print('v3/intro_pids', ([p['product_id'] for p in result['intro_plans']]))

        print("==> fetch_plan_config_lite")
        result = bryo.app.iap.fetch_plan_config_lite(
            self.user_id,
            self.platform,
            self.code_name,
            '10.0.0')
        print('lite/pids', ([p['product_id'] for p in result['plans']]))
        print('lite/intro_pids', ([p['product_id'] for p in result['intro_plans']]))


tester = PremiumTester('vicky@glowing.com',
                       platform='ios',
                       code_name='emma',
                       app_version="12.0.0",
                       host_app_code_name='emma',
                       host_app_version="12.0.0",
                       rn_version='5.0.0',
                       )
main(tester)
