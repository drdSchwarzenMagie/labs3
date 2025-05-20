<?php
use yii\widgets\ActiveForm;
use yii\helpers\Html;
$this->title = 'Добавить подпись';
?>
<h1><?= Html::encode($this->title) ?></h1>

<img src="/upload/<?= Html::encode($model->filename) ?>" width="200"><br>

<?php $form = ActiveForm::begin(); ?>
    <?= $form->field($model, 'caption')->textarea(['rows' => 2]) ?>
    <div class="form-group">
        <?= Html::submitButton('Сохранить подпись', ['class' => 'btn btn-success']) ?>
    </div>
<?php ActiveForm::end(); ?>
