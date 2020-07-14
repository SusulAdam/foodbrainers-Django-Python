// navigation

let navigation = document.querySelector('.navigation');

// ruch myszki
window.addEventListener('scroll', function () {
    let scrollYPostion = window.pageYOffset;

    if (scrollYPostion > 50) {
        navigation.classList.add('move');
    }

    else {
        navigation.classList.remove('move');
    }

}

) // Slider
const slider = document.querySelector('.slider__puictures');
const sliderImages = document.querySelectorAll('.slider__puicture img');
const prevBtn = document.querySelector('.fa-arrow-circle-left');
const nextBtn = document.querySelector('.fa-arrow-circle-right');

let counter = 1;

const size = sliderImages[0].clientWidth;

slider.style.transform = 'translateX(' + (-size * counter) + 'px)';

//Button Lisiners

nextBtn.addEventListener('click', () => {
    if (counter >= sliderImages.length - 1) return;
    slider.style.transition = "transform 0.3s ease-in-out";
    counter++;
    slider.style.transform = 'translateX(' + (-size * counter) + 'px)';
}

);

prevBtn.addEventListener('click', () => {
    if (counter <= 0) return;
    slider.style.transition = "transform 0.3s ease-in-out";
    counter--;

    slider.style.transform = 'translateX(' + (-size * counter) + 'px)';
}

);

slider.addEventListener('transitionend', () => {

    if (sliderImages[counter].classList == 'last') {
        slider.style.transition = "none";
        counter = sliderImages.length - 2;
        slider.style.transform = 'translateX(' + (-size * counter) + 'px)';
    }

    if (sliderImages[counter].classList == 'first') {
        slider.style.transition = "none";
        counter = sliderImages.length - counter;
        slider.style.transform = 'translateX(' + (-size * counter) + 'px)';
    }
}

);

// Api Map

function initMap() {
    let latitude = JSON.parse(document.getElementById('lat').textContent);
    let logitude = JSON.parse(document.getElementById('lng').textContent);
    var options = {

        zoom: 14,
        center: {
            lat: latitude, lng: logitude
        }
    }
    var map = new google.maps.Map(document.getElementById('map'), options);

    var marker = new google.maps.Marker({
        position: { lat: latitude, lng: logitude },
        map: map
    })
}