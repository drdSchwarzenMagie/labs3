<?php
class SiteControllerCest
{
    public function _before(\FunctionalTester $I)
    {
        $I->amOnRoute('site/index');
    }

}
