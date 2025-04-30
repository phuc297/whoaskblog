
document.addEventListener('DOMContentLoaded', function () {

	const tabs = document.querySelectorAll('.tab-item')

	tabs.forEach((tab, index) => {

		tab.addEventListener('click', function (event) {

			tabs.forEach((t) => t.classList.remove('text-green-500', 'border-green-500', 'active', 'border-b-2'))

			this.classList.add('text-green-500', 'border-b-2', 'border-green-500', 'active')

		})

	})

})