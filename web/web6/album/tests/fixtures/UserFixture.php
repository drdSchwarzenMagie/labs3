<?php
namespace app\tests\fixtures;

use yii\test\ActiveFixture;

class UserFixture extends ActiveFixture
{
    public $modelClass = 'app\\models\\User';
    public $dataFile = __DIR__ . '/../_data/users.php';
}