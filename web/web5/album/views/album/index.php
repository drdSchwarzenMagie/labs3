<?php
use yii\helpers\Html;
use yii\helpers\Url;
use yii\widgets\ActiveForm;
$this->title = 'Мой альбом';
?>
<h1><?= Html::encode($this->title) ?></h1>

<!-- Кнопка загрузки фото -->
<p>
    <a href="<?= Url::to(['album/upload']) ?>" class="btn btn-success">Загрузить фотографию</a>
</p>

<h2>Мои изображения</h2>
<div>
    <?php foreach ($myImages as $img): ?>
        <div style="display:inline-block;margin:10px;text-align:center;vertical-align:top;">
            <img src="/upload/<?= Html::encode($img->filename) ?>" width="150" class="img-thumbnail album-thumb" style="cursor:zoom-in" data-full="/upload/<?= Html::encode($img->filename) ?>"><br>
            <div style="margin:5px 0;">
                <?= Html::encode($img->caption) ?><br>
            </div>
            <?php if ($img->owner == Yii::$app->user->identity->login): ?>
                <a href="<?= Url::to(['album/delete', 'id' => $img->id]) ?>" class="btn btn-danger btn-sm">Удалить</a>
            <?php endif; ?>
        </div>
    <?php endforeach; ?>
</div>



<hr>

<!-- Увеличение фото -->
<div class="modal fade" id="imgModal" tabindex="-1" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content">
      <div class="modal-body p-0 text-center">
        <img id="modalImg" src="" style="max-width:100%;max-height:80vh;">
      </div>
    </div>
  </div>
</div>

<?php
$this->registerJs(<<<JS
$('.album-thumb').on('click', function() {
  $('#modalImg').attr('src', $(this).data('full'));
  $('#imgModal').modal('show');
});
JS
);
?>
