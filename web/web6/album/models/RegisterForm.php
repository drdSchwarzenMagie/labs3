<?php
namespace app\models;

use yii\base\Model;
use app\models\User;

class RegisterForm extends Model
{
    public $login;
    public $password;
    public $password_repeat;

    public function rules()
    {
        return [
            [['login', 'password', 'password_repeat'], 'required'],
            ['login', 'unique', 'targetClass' => User::class, 'targetAttribute' => 'login', 'message' => 'Этот логин уже занят.'],
            ['password', 'string', 'min' => 4],
            ['password_repeat', 'compare', 'compareAttribute' => 'password', 'message' => 'Пароли не совпадают.'],
        ];
    }

    public function register()
    {
        if (!$this->validate()) {
            return false;
        }
        
        $user = new User();
        $user->login = $this->login;
        $user->password = md5($this->password);
        
        return $user->save(false);
    }
}
