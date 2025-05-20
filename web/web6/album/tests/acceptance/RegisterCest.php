<?php
use yii\helpers\Url;

class RegisterCest
{
    public function ensureThatRegisterPageWorks(AcceptanceTester $I)
    {
        $I->amOnPage(Url::toRoute('/register/index'));
        $I->see('Register', 'h1');
    }

    public function registerFromUI(AcceptanceTester $I)
    {
        $I->amOnPage(Url::toRoute('/register/index'));
        $I->fillField('input[name="RegisterForm[username]"]', 'uiuser');
        $I->fillField('input[name="RegisterForm[email]"]', 'uiuser@example.com');
        $I->fillField('input[name="RegisterForm[password]"]', 'uipassword');
        $I->click('register-button');
        $I->see('Registration successful');
    }
}
