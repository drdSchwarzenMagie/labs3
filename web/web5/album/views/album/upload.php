<?php
use yii\widgets\ActiveForm;
use yii\helpers\Html;
$this->title = 'Загрузка изображения';
?>
<h1><?= Html::encode($this->title) ?></h1>

<?php $form = ActiveForm::begin(['options' => ['enctype' => 'multipart/form-data']]); ?>
    <?= $form->field($model, 'imageFile')->fileInput() ?>
    <div class="form-group">
        <?= Html::submitButton('Загрузить', ['class' => 'btn btn-primary']) ?>
    </div>
<?php ActiveForm::end(); ?>
