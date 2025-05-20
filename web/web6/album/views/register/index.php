<?php
use yii\helpers\Html;
use yii\widgets\ActiveForm;
$this->title = 'Регистрация';
?>
<h1><?= Html::encode($this->title) ?></h1>

<div class="row">
    <div class="col-lg-5">
        <?php $form = ActiveForm::begin(['id' => 'register-form']); ?>
            <?= $form->field($model, 'login')->textInput(['autofocus' => true]) ?>
            <?= $form->field($model, 'password')->passwordInput() ?>
            <?= $form->field($model, 'password_repeat')->passwordInput() ?>
            <div class="form-group">
                <?= Html::submitButton('Зарегистрироваться', ['class' => 'btn btn-success', 'name' => 'register-button']) ?>
            </div>
        <?php ActiveForm::end(); ?>
    </div>
</div>
