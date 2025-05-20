<?php
use yii\helpers\Url;

class ImageFormCest
{
    public function ensureThatImageFormWorks(AcceptanceTester $I)
    {
        $I->amOnPage(Url::toRoute('/album/create'));
        $I->see('Create Image', 'h1');
        $I->seeElement('form#image-form');
    }

    public function submitImageFormWithErrors(AcceptanceTester $I)
    {
        $I->amOnPage(Url::toRoute('/album/create'));
        $I->click('save-button');
        $I->see('Filename cannot be blank');
    }
}
