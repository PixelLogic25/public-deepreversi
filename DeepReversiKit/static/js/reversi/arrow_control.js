//矢印の非表示を管理する。

class ArrowControl{

    constructor(){
        this.board_arrow = document.getElementById("game-start-yuudou-arrow-area");//盤面上のほうの矢印
        this.board_arrow_button = document.getElementById("yuudou-arrow-close-button");//盤面上のほうの矢印を消すボタン
        const game_start_button_target = document.getElementById("game-start-button");//対局開始ボタン

        this.start_arrow = document.getElementById("game-start-arrow");//下の方にある対局開始ボタンの矢印
        
        this.board_arrow_button.addEventListener('click', (event) =>{
        
            this.noneDisplayYuudou();
        
        });

        game_start_button_target.addEventListener('click', (event) =>{//対局開始ボタンを押したとき
            this.start_arrow.style.display = "none";

        });

        this.observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
              if (entry.isIntersecting) {
                this.noneDisplayYuudou();
              }
            });
          }, {
            root: null,           // ビューポートが基準
            threshold: 0.1        // 10%以上見えたら反応（お好みで）
          });
          
        this.observer.observe(game_start_button_target);
    }
    
    
    noneDisplayYuudou(){

        this.board_arrow.style.display = "none";
    }


}


