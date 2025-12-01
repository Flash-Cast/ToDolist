// 1. 型定義
type Todo = {
  id: number;
  text: string;
  isCompleted: boolean;
};

// 2. 状態管理（データ）
let todos: Todo[] = [];

// 3. DOM要素の取得
// HTMLの要素を取得します。"as HTML..." をつけて型を明示します。
const inputEl = document.getElementById('todo-input') as HTMLInputElement;
const addButtonEl = document.getElementById('add-button') as HTMLButtonElement;
const listEl = document.getElementById('todo-list') as HTMLUListElement;

// 4. 画面描画関数（データをもとにHTMLを書き換える）
const renderTodos = () => {
  // 一旦リストの中身を空にする
  listEl.innerHTML = '';

  todos.forEach((todo) => {
    // liタグを作成
    const li = document.createElement('li');

    // テキスト表示部分
    const span = document.createElement('span');
    span.textContent = todo.text;
    span.style.cursor = 'pointer';
    if (todo.isCompleted) {
      span.classList.add('completed'); // CSSクラスを付与
    }

    // クリックで完了状態を切り替え
    span.addEventListener('click', () => {
      toggleTodo(todo.id);
    });

    // 削除ボタン
    const deleteBtn = document.createElement('button');
    deleteBtn.textContent = '削除';
    deleteBtn.style.marginLeft = '10px';

    // クリックで削除
    deleteBtn.addEventListener('click', () => {
      deleteTodo(todo.id);
    });

    // liに要素を追加して、さらにulに追加
    li.appendChild(span);
    li.appendChild(deleteBtn);
    listEl.appendChild(li);
  });
};

// 5. ロジック関数（データを操作する）

// Todoを追加する
const addTodo = () => {
  const text = inputEl.value;
  if (text === '') return;

  const newTodo: Todo = {
    id: Date.now(),
    text: text,
    isCompleted: false,
  };

  todos.push(newTodo);
  inputEl.value = ''; // 入力欄をクリア
  renderTodos(); // 再描画
};

// Todoを完了/未完了にする
const toggleTodo = (id: number) => {
  const todo = todos.find((t) => t.id === id);
  if (todo) {
    todo.isCompleted = !todo.isCompleted;
    renderTodos(); // 再描画
  }
};

// Todoを削除する
const deleteTodo = (id: number) => {
  todos = todos.filter((t) => t.id !== id);
  renderTodos(); // 再描画
};

// 6. イベントリスナーの設定
// ボタンクリック時
addButtonEl.addEventListener('click', addTodo);

// エンターキーでも追加できるようにする
inputEl.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    addTodo();
  }
});