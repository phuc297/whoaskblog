document.addEventListener('DOMContentLoaded', function (event) {
    const btn = document.getElementById('dropdown-profile-button')
    const menu = document.getElementById('dropdown-profile-menu')

    btn.addEventListener('click', function (event) {
        menu.classList.toggle('hidden')
    })
})

document.addEventListener('click', function (event) {
    const btn = document.getElementById('dropdown-profile-button')
    const menu = document.getElementById('dropdown-profile-menu')
    const isClickInside = menu.contains(event.target) || btn.contains(event.target)
    if (!isClickInside) {
        menu.classList.add('hidden')
    }
})

document.addEventListener('DOMContentLoaded', function (event) {
    const btn = document.getElementById('dropdown-notification-button')
    const menu = document.getElementById('dropdown-notification-menu')

    btn.addEventListener('click', function (event) {
        menu.classList.toggle('hidden')
    })
})

document.addEventListener('click', function (event) {
    const btn = document.getElementById('dropdown-notification-button')
    const menu = document.getElementById('dropdown-notification-menu')
    const isClickInside = menu.contains(event.target) || btn.contains(event.target)
    if (!isClickInside) {
        menu.classList.add('hidden')
    }
})