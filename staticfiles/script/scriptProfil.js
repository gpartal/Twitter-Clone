const postes = document.querySelectorAll(".postes");

for(let post of postes) {
    post.addEventListener("click", () => {
        this.children.children[1].classList.remove("bg-primary");
    });
}
