<?php

use app\tests\fixtures\UserFixture;

class RegisterControllerCest
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
        $I->amOnRoute('register/index');
    }

    public function openRegisterPage(\FunctionalTester $I)
    {
        $I->see('Регистрация', 'h1');
    }

    public function submitRegisterForm(\FunctionalTester $I)
    {
        $I->submitForm('#register-form', [
            'RegisterForm[login]' => 'newuser',
            'RegisterForm[password]' => 'testpass',
            'RegisterForm[password_repeat]' => 'testpass',
        ]);
        $I->see('Регистрация прошла успешно! Теперь вы можете войти.');
    }
}
