<?php
use yii\helpers\Html;
use yii\widgets\ActiveForm;
$this->title = 'Удаление изображения';
?>
<h1><?= Html::encode($this->title) ?></h1>

<img src="/upload/<?= Html::encode($model->filename) ?>" width="200"><br>
<p><?= Html::encode($model->caption) ?></p>

<?php $form = ActiveForm::begin(); ?>
    <p>Действительно удалить?</p>
    <input type="hidden" name="confirm" value="yes">
    <div class="form-group">
        <?= Html::submitButton('Удалить', ['class' => 'btn btn-danger']) ?>
        <a href="<?= Yii::$app->urlManager->createUrl(['album/index']) ?>" class="btn btn-default">Отмена</a>
    </div>
<?php ActiveForm::end(); ?>
