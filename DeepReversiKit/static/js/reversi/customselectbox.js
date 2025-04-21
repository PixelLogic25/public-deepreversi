class CustomSelectBox {
    constructor(element) {
        this.element = element; // カスタムセレクトボックスのルート要素
        this.options = JSON.parse(element.getAttribute('data-options') || '[]'); // オプションデータ
        this.placeholder = element.getAttribute('data-placeholder') || '選択してください';
        this.selectedValue = null; // 現在選択されている値

        this.init(); // 初期化処理
    }

    // 初期化処理
    init() {
        // UIを構築
        this.render();

        // イベントリスナーを設定
        this.setupEventListeners();
    }

    // UIを構築
    render() {
        // 既存の内容をクリア
        this.element.innerHTML = '';

        // コンテナを作成
        this.container = document.createElement('div');
        this.container.classList.add('custom-select-container');
        this.element.appendChild(this.container);

        // プレースホルダーを作成
        this.placeholderElement = document.createElement('div');
        this.placeholderElement.classList.add('custom-select-placeholder');
        this.placeholderElement.textContent = this.placeholder;
        this.container.appendChild(this.placeholderElement);

        // 選択肢リストを作成
        this.optionsList = document.createElement('ul');
        this.optionsList.classList.add('custom-select-options');
        this.options.forEach(option => this.createOptionElement(option));
        this.container.appendChild(this.optionsList);
    }

    // 選択肢のDOM要素を作成
    createOptionElement(option) {
        const listItem = document.createElement('li');
        listItem.textContent = option.label;
        listItem.setAttribute('data-value', option.value);
        listItem.classList.add('custom-select-option');
        if (this.selectedValue === option.value) {
            listItem.classList.add('selected'); // 既に選択されている場合はスタイルを適用
        }
        this.optionsList.appendChild(listItem);
    }

    // イベントリスナーを設定
    setupEventListeners() {
        // プレースホルダーのクリックで選択肢を表示・非表示
        this.placeholderElement.addEventListener('click', () => {
            this.optionsList.classList.toggle('visible');
        });

        // 選択肢をクリックしたときの処理
        this.optionsList.addEventListener('click', (e) => {
            const item = e.target.closest('.custom-select-option');
            if (!item) return;

            // 他の選択肢を解除
            this.optionsList.querySelectorAll('.selected').forEach(selectedItem => {
                selectedItem.classList.remove('selected');
            });

            // 新しい選択を適用
            item.classList.add('selected');
            this.selectedValue = item.getAttribute('data-value');
            this.placeholderElement.textContent = item.textContent;

            // 選択肢リストを非表示
            this.optionsList.classList.remove('visible');

            // 選択イベントの通知
            this.onSelect(this.selectedValue);
        });

        // 外部クリックでリストを閉じる
        document.addEventListener('click', (e) => {
            if (!this.container.contains(e.target)) {
                this.optionsList.classList.remove('visible');
            }
        });
    }

    // 動的に項目を追加する
    addOption(option) {
        this.options.push(option); // オプションデータに追加
        this.createOptionElement(option); // DOMに追加
    }

    // 選択肢リスト全体を更新する
    updateOptions(newOptions) {
        this.options = newOptions; // 新しいオプションデータをセット
        this.render(); // UIを再構築
    }

    // 選択されたときのコールバック（必要に応じてオーバーライド）
    onSelect(value) {
        console.log('選択された値:', value);
    }
}