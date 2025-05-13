<?php
namespace app\models;

use Yii;
use yii\db\ActiveRecord;
use yii\web\UploadedFile;

/**
 * This is the model class for table "images".
 *
 * @property int $id
 * @property string $filename
 * @property string $caption
 * @property string $owner
 * @property int $is_public
 * @property string $created_at
 */
class Image extends ActiveRecord
{
    /**
     * @var UploadedFile
     */
    public $imageFile;

    public static function tableName()
    {
        return 'images';
    }

    public function rules()
    {
        return [
            [['filename', 'owner'], 'required'],
            [['caption'], 'string', 'max' => 25, 'tooLong' => 'Описание не должно превышать 25 символов.'],
            [['created_at'], 'safe'],
            [['filename', 'owner'], 'string', 'max' => 255],
            [['imageFile'], 'file', 'skipOnEmpty' => true, 'extensions' => 'png, jpg, jpeg, gif'],
        ];
    }

    public function upload()
    {
        if ($this->validate()) {
            $filename = Yii::getAlias('@webroot/upload/') . $this->filename;
            return $this->imageFile->saveAs($filename);
        }
        return false;
    }
}
