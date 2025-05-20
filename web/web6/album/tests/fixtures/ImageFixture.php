<?php
namespace app\tests\fixtures;

use yii\test\ActiveFixture;

class ImageFixture extends ActiveFixture
{
    public $modelClass = 'app\\models\\Image';
    public $dataFile = __DIR__ . '/../_data/image.php';
}