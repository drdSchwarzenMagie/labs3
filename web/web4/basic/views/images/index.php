<?php

use app\models\Images;
use yii\helpers\Html;
use yii\helpers\Url;
use yii\grid\ActionColumn;
use yii\grid\GridView;

/** @var yii\web\View $this */
/** @var app\models\ImagesSearch $searchModel */
/** @var yii\data\ActiveDataProvider $dataProvider */

$this->title = 'Images';
$this->params['breadcrumbs'][] = $this->title;
?>
<div class="images-index">

    <h1><?= Html::encode($this->title) ?></h1>

    <p>
        <?= Html::a('Create Images', ['create'], ['class' => 'btn btn-success']) ?>
    </p>

    <?php // echo $this->render('_search', ['model' => $searchModel]); ?>

    <?= GridView::widget([
        'dataProvider' => $dataProvider,
        'filterModel' => $searchModel,
        'layout' => "{items}\n{summary}",
        'columns' => [
            ['class' => 'yii\grid\SerialColumn'],

            'id',
            'name',
            'caption',
            [
                'class' => ActionColumn::className(),
                'urlCreator' => function ($action, Images $model, $key, $index, $column) {
                    return Url::toRoute([$action, 'id' => $model->id]);
                 }
            ],
        ],
    ]); ?>
    <?= \yii\widgets\LinkPager::widget([
    'pagination' => $dataProvider->pagination,
    'options' => ['class' => 'pagination justify-content-center'], // Центрирование пагинации
    'linkOptions' => ['class' => 'page-link'], // Стиль ссылок
    'disabledPageCssClass' => 'disabled', // Неактивные страницы
    'activePageCssClass' => 'active', // Активная страница
    'prevPageLabel' => '«', // Иконка для предыдущей страницы
    'nextPageLabel' => '»', // Иконка для следующей страницы
]) ?>


</div>
