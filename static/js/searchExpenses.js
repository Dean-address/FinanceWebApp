const searchField = document.querySelector('#searchField')
const tableOutput = document.querySelector('.table-output')
const appTable = document.querySelector('.app-table')
const paginationContainer = document.querySelector('.pagination-container')
const tableBody = document.querySelector('.table-body')
tableOutput.style.display = 'none'
searchField.addEventListener('keyup', (e) => {
	const searchValue = e.target.value;


	if (searchValue.trim().length > 0) {
		paginationContainer.style.display = 'none';
		tableBody.innerHTML = ''
		fetch('/search_expenses', {
			body: JSON.stringify({ searchText: searchValue }),
			method: 'POST'
		}).then(res => res.json()).then((data) => {
			console.log(data)
			appTable.style.display = 'none';
			tableOutput.style.display = 'block';

			if (data.length === 0) {
				tableOutput.innerHTML = 'No result found'

			} else {
				data.forEach(item => {
					tableBody.innerHTML += `
						<td>${item.amount}</td>
						<td>${item.category}</td>
						<td>${item.description}</td>
						<td>${item.date}</td>
						<td>

							<a href={{% url 'expenses:edit_expenses' ${item.id} %}}
			class="btn btn-sm btn-secondary" > Edit</a >
				<a href="{% url 'expenses:delete_expenses' expense.id %}"
					class="btn btn-sm btn-danger">Delete</a>
						</td >

				`
				})


			}

		})
	} else {
		appTable.style.display = 'block';
		paginationContainer.style.display = 'block';
		tableOutput.style.display = 'none'



	}

})