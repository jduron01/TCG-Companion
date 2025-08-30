function displayGallery() {
    let idx = 0;

    showImages(idx);

    window.changeImage = n => {
        showImages(idx += n);
    }
};

function showImages(n) {
    const gallery = document.getElementsByClassName("Gallery");
    const cardsPerPage = 6;
    const totalCards = gallery.length;

    if (n >= totalCards) {
        idx = 0;
    } else if (n < 0) {
        idx = totalCards - cardsPerPage;
    }

    for (let i = 0; i < totalCards; i++) {
        gallery[i].style.display = "none";
    }

    for (let i = idx; i < idx + cardsPerPage && i < totalCards; i++) {
        gallery[i].style.display = "block";
    }
}