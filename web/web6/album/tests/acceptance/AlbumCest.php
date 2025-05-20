<?php
use yii\helpers\Url;

class AlbumCest
{
    public function ensureThatAlbumPageWorks(AcceptanceTester $I)
    {
        $I->amOnPage(Url::toRoute('/album/index'));
        $I->see('Album', 'h1');
    }

    public function createImageFromUI(AcceptanceTester $I)
    {
        $I->amOnPage(Url::toRoute('/album/create'));
        $I->fillField('input[name="Image[filename]"]', 'ui_test.jpg');
        $I->fillField('input[name="Image[title]"]', 'UI Test Image');
        $I->click('save-button');
        $I->see('Image saved');
    }

    public function viewImageFromUI(AcceptanceTester $I)
    {
        $I->amOnPage(Url::toRoute('/album/view?id=1'));
        $I->see('UI Test Image');
    }
}
