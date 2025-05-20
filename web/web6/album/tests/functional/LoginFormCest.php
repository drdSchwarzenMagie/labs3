<?php

use app\tests\fixtures\UserFixture;

class LoginFormCest
{
    public function _fixtures()
    {
        return [
            'users' => [
                'class' => UserFixture::class,
            ],
        ];
    }
    
    public function _before(\FunctionalTester $I)
    {
        $I->amOnRoute('site/login');
    }

    public function openLoginPage(\FunctionalTester $I)
    {
        $I->see('Login', 'h1');
    }

    public function internalLoginById(\FunctionalTester $I)
    {
        $I->amLoggedInAs(1);
        $I->amOnRoute('album/index');
        $I->see('Logout (testuser)');
    }

    public function internalLoginByInstance(\FunctionalTester $I)
    {
        $user = \app\models\User::findByUsername('testuser');
        $I->amLoggedInAs($user);
        $I->amOnRoute('album/index');
        $I->see('Logout (testuser)');
    }

    public function loginWithEmptyCredentials(\FunctionalTester $I)
    {
        $I->submitForm('#login-form', []);
        $I->expectTo('see validations errors');
        $I->see('Login cannot be blank.');
        $I->see('Password cannot be blank.');
    }

    public function loginWithWrongCredentials(\FunctionalTester $I)
    {
        $I->submitForm('#login-form', [
            'LoginForm[login]' => 'testuser',
            'LoginForm[password]' => 'wrong',
        ]);
        $I->expectTo('see validations errors');
        $I->see('Incorrect login or password.');
    }

    public function loginSuccessfully(\FunctionalTester $I)
    {
        $I->submitForm('#login-form', [
            'LoginForm[login]' => 'testuser',
            'LoginForm[password]' => 'password',
        ]);
        $I->see('Logout (testuser)');
        $I->dontSeeElement('form#login-form');              
    }
}