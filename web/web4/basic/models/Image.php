<?php
namespace app\models;

use Yii;

/**
 * This is the model class for table "images".
 *
 * @property int $id
 * @property string|null $name
 * @property string|null $caption
 */
class Image extends \yii\db\ActiveRecord
{
    /**
     * {@inheritdoc}
     */
    public static function tableName()
    {
        return 'images'; // Имя таблицы в базе данных
    }

    /**
     * {@inheritdoc}
     */
    public function rules()
    {
        return [
            [['name', 'caption'], 'string', 'max' => 256], // Правила для полей
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function attributeLabels()
    {
        return [
            'id' => 'ID',
            'name' => 'Name',
            'caption' => 'Caption',
        ];
    }
}

