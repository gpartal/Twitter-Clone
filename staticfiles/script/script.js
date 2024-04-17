const private = document.getElementById("private");
const follows = document.getElementById("follows");

private.addEventListener("click", () => {
    private.children[0].children[1].classList.add("bg-primary");
    follows.children[0].children[1].classList.remove("bg-primary");
});

follows.addEventListener("click", () => {
    follows.children[0].children[1].classList.add("bg-primary");
    private.children[0].children[1].classList.remove("bg-primary");
});

function openTab(evt, cityName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
  }