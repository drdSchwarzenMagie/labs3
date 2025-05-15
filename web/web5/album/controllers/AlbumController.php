<?php
namespace app\controllers;

use Yii;
use yii\web\Controller;
use yii\filters\AccessControl;
use yii\web\UploadedFile;
use app\models\Image;
use app\models\LoginForm;

class AlbumController extends Controller
{
    public function behaviors()
    {
        return [
            'access' => [
                'class' => AccessControl::class,
                'only' => ['index', 'upload', 'delete', 'view'],
                'rules' => [
                    [
                        'allow' => true,
                        'roles' => ['@'],
                    ],
                ],
            ],
        ];
    }

    //  C2: Главная страница
    public function actionIndex()
    {
        // Разделяем изображения на личные и публичные
        $myImages = Image::find()->where(['owner' => Yii::$app->user->identity->login])->all();
        return $this->render('index', [
            'myImages' => $myImages,
        ]);
    }

    // C3: Загрузка новой фотографии
    public function actionUpload()
    {
        $model = new Image();
        if (Yii::$app->request->isPost) {
            $model->imageFile = UploadedFile::getInstance($model, 'imageFile');
            if ($model->imageFile) {
                $model->filename = uniqid() . '.' . $model->imageFile->extension;
                $model->owner = Yii::$app->user->identity->login;
                $model->created_at = date('Y-m-d H:i:s');
                if ($model->upload() && $model->save(false)) {
                    return $this->redirect(['caption', 'id' => $model->id]);
                }
            }
        }
        return $this->render('upload', ['model' => $model]);
    }

    // C3: Добавление подписи к загруженной фотографии
    public function actionCaption($id)
    {
        $model = Image::findOne($id);
        if (!$model || $model->owner !== Yii::$app->user->identity->login) {
            throw new \yii\web\ForbiddenHttpException('Access denied');
        }
        if (Yii::$app->request->isPost && $model->load(Yii::$app->request->post())) {
            $model->save(false);
            return $this->redirect(['index']);
        }
        return $this->render('caption', ['model' => $model]);
    }

    // C4: Подтверждение удаления
    public function actionDelete($id)
    {
        $model = Image::findOne($id);
        if (!$model || $model->owner !== Yii::$app->user->identity->login) {
            throw new \yii\web\ForbiddenHttpException('Access denied');
        }
        if (Yii::$app->request->isPost && Yii::$app->request->post('confirm') === 'yes') {
            $file = Yii::getAlias('@webroot/upload/') . $model->filename;
            if (file_exists($file)) {
                unlink($file);
            }
            $model->delete();
            return $this->redirect(['index']);
        }
        return $this->render('delete', ['model' => $model]);
    }
    
}
