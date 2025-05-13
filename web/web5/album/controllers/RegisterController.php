<?php
namespace app\controllers;

use Yii;
use yii\web\Controller;
use app\models\RegisterForm;
use app\models\User;

class RegisterController extends Controller
{
    public function actionIndex()
    {
        $model = new RegisterForm();
        if ($model->load(Yii::$app->request->post()) && $model->validate()) {
            $user = new User();
            $user->login = $model->login;
            $user->password = md5($model->password);
            if ($user->save(false)) {
                Yii::$app->session->setFlash('success', 'Регистрация прошла успешно! Теперь вы можете войти.');
                return $this->redirect(['site/login']);
            } else {
                Yii::$app->session->setFlash('error', 'Ошибка при сохранении пользователя.');
            }
        }
        return $this->render('index', ['model' => $model]);
    }
}
