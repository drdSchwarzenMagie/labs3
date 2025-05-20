<?php

namespace tests\unit\models;

use app\models\User;
use app\tests\fixtures\UserFixture;

class UserTest extends \Codeception\Test\Unit
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

    public function testFindUserById()
    {
        verify($user = User::findIdentity(1))->notEmpty();
        verify($user->login)->equals('testuser');
        verify(User::findIdentity(999))->empty();
    }

    public function testFindUserByUsername()
    {
        verify($user = User::findByUsername('testuser'))->notEmpty();
        verify(User::findByUsername('not-admin'))->empty();
    }
    
    public function testValidatePassword()
    {
        $user = User::findByUsername('testuser');
        verify($user->validatePassword('password'))->true();
        verify($user->validatePassword('wrong-password'))->false();
    }

    public function testInvalidPassword()
    {
        $user = User::findByUsername('testuser');
        $this->assertFalse($user->validatePassword('incorrect'));
        $this->assertNotFalse($user->validatePassword('password'));
    }
    
}