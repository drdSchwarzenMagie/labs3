<?php

use app\tests\fixtures\UserFixture;
use app\tests\fixtures\ImageFixture;

class AlbumControllerCest
{
    public function _fixtures()
    {
        return [
            'users' => [
                'class' => UserFixture::class,
            ],
            'images' => [
                'class' => ImageFixture::class,
            ],
        ];
    }
    
    public function _before(\FunctionalTester $I)
    {
        $I->amOnRoute('site/login');
        $I->submitForm('#login-form', [
            'LoginForm[login]' => 'testuser',
            'LoginForm[password]' => 'password',
        ]);
        $I->amOnRoute('album/index');
    }

    public function ensureIndexWorks(\FunctionalTester $I)
    {
        $I->see('Мой альбом', 'h1');
    }

    public function uploadImageSuccessfully(\FunctionalTester $I)
    {
        $I->amOnRoute('album/upload');
        $I->see('Загрузка изображения', 'h1');
        $I->seeElement('input[name="Image[imageFile]"]');
    }


    public function deleteImage(\FunctionalTester $I)
    {
        $I->amOnRoute('album/delete', ['id' => 1]);
        $I->see('Удаление изображения', 'h1');
        $I->submitForm('form', ['confirm' => 'yes']);
        $I->amOnRoute('album/index');
        $I->dontSee('To delete');
    }

}
