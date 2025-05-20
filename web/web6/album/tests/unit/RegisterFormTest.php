<?php

namespace tests\unit\models;

use app\models\RegisterForm;
use app\models\User;
use app\tests\fixtures\UserFixture;
use Codeception\Test\Unit;

class RegisterFormTest extends Unit
{
    /**
     * @return array
     */
    public function _fixtures()
    {
        return [
            'users' => [
                'class' => UserFixture::class,
            ],
        ];
    }
    
    public function _before()
    {
        User::deleteAll();
    }
    
    public function testRegisterSuccess()
    {
        $model = new RegisterForm([
            'login' => 'newuser',
            'password' => 'securepassword',
            'password_repeat' => 'securepassword',
        ]);
        $this->assertTrue($model->validate());
        $this->assertTrue($model->register());
    }

    public function testRegisterValidationFails()
    {
        $model = new RegisterForm([
            'login' => '',
            'password' => '',
            'password_repeat' => '',
        ]);
        $this->assertFalse($model->validate());
        $this->assertArrayHasKey('login', $model->errors);
        $this->assertArrayHasKey('password', $model->errors);
        $this->assertArrayHasKey('password_repeat', $model->errors);
    }

    public function testDuplicateUsernameOrEmail()
    {
        $model1 = new RegisterForm([
            'login' => 'duplicate',
            'password' => 'password',
            'password_repeat' => 'password',
        ]);
        $model1->register();
        
        $model2 = new RegisterForm([
            'login' => 'duplicate',
            'password' => 'password',
            'password_repeat' => 'password',
        ]);
        $this->assertFalse($model2->validate());
        $this->assertArrayHasKey('login', $model2->errors);
    }

    public function testPasswordMinLength()
    {
        $form = new RegisterForm([
            'login' => 'user1',
            'password' => '123',
            'password_repeat' => '123'
        ]);

        $this->assertFalse($form->validate());
        $this->assertArrayHasKey('password', $form->errors);
    }

    public function testPasswordRepeatMatches()
    {
        $form = new RegisterForm([
            'login' => 'user1',
            'password' => 'pass123',
            'password_repeat' => 'wrongpass'
        ]);

        $this->assertFalse($form->validate());
        $this->assertArrayHasKey('password_repeat', $form->errors);
        $this->assertEquals('Пароли не совпадают.', $form->errors['password_repeat'][0]);
    }
}
