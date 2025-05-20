<?php

namespace tests\unit\models;

use app\models\Image;
use app\tests\fixtures\ImageFixture;
use app\tests\fixtures\UserFixture;
use Codeception\Test\Unit;
use yii\web\UploadedFile;

class ImageTest extends Unit
{
    /**
     * @return array
     */
    public function _fixtures()
    {
        return [
            'images' => [
                'class' => ImageFixture::class,
            ],
            'users' => [
                'class' => UserFixture::class,
            ],
        ];
    }
    
    public function testCreateImage()
    {
        $image = new Image([
            'filename' => 'test.jpg',
            'owner' => 'testuser',
            'caption' => 'Test image',
        ]);
        $this->assertTrue($image->validate());
    }

    public function testImageValidationFails()
    {
        $image = new Image([
            'filename' => '', 
            'owner' => null,
        ]);
        $this->assertFalse($image->validate());
        $this->assertArrayHasKey('filename', $image->errors);
        $this->assertArrayHasKey('owner', $image->errors);
    }

    public function testSaveAndFindImage()
    {
        $image = new Image([
            'filename' => 'test_fixture.jpg',
            'owner' => 'testuser',
            'caption' => 'Fixture Test',
            'created_at' => date('Y-m-d H:i:s')
        ]);
        $this->assertTrue($image->save(false));
        $found = Image::findOne(['filename' => 'test_fixture.jpg']);
        $this->assertNotNull($found);
        $this->assertEquals('test_fixture.jpg', $found->filename);
        $this->assertEquals('Fixture Test', $found->caption);
    }

    public function testDeleteImage()
    {
        $image = Image::findOne(1); 
        $this->assertNotNull($image, 'Изображение из фикстуры не найдено');
        $id = $image->id;
        $image->delete();
        $this->assertNull(Image::findOne($id));
    }

    public function testFilenameMaxLength()
    {
        $image = new Image([
            'filename' => str_repeat('a', 256),
            'owner' => 'testuser'
        ]);

        $this->assertFalse($image->validate());
        $this->assertArrayHasKey('filename', $image->errors);
    }

    public function testOwnerMaxLength()
    {
        $image = new Image([
            'owner' => str_repeat('a', 256),
            'filename' => 'test.jpg'
        ]);

        $this->assertFalse($image->validate());
        $this->assertArrayHasKey('owner', $image->errors);
    }

    public function testCaptionMaxLength()
    {
        $image = new Image([
            'caption' => str_repeat('a', 26),
            'filename' => 'test.jpg',
            'owner' => 'testuser'
        ]);

        $this->assertFalse($image->validate());
        $this->assertArrayHasKey('caption', $image->errors);
    }

    public function testInvalidExtensionUpload()
    {
        $file = new UploadedFile([
            'name' => 'test.php',
            'tempName' => codecept_data_dir('fixtures/test.php'),
            'size' => 1024,
            'type' => 'application/x-msdownload',
            'error' => UPLOAD_ERR_OK,
        ]);

        $image = new Image();
        $image->imageFile = $file;

        $this->assertFalse($image->validate(['imageFile']));
        $this->assertArrayHasKey('imageFile', $image->errors);
    }

    public function testValidImageUpload()
    {
        $file = new UploadedFile([
            'name' => 'test.png',
            'tempName' => codecept_data_dir('fixtures/test.png'),
            'size' => 1024,
            'type' => 'image/png',
            'error' => UPLOAD_ERR_OK,
        ]);

        $image = new Image();
        $image->imageFile = $file;
        $image->filename = 'test.png';
        $image->owner = 'testuser';

        $this->assertTrue($image->validate(['imageFile']));
    }
    
}
