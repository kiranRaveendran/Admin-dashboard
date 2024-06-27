

function remove_hidden(){
    document.getElementById ('delete-modal').classList.remove('hidden');
}

function add_hidden(){
    document.getElementById('delete-modal').classList.add('hidden');
}

function Edit_function(e, pk){
    e.preventDefault();
    remove_hidden();
    primary(pk)
    $.ajax({
        type: 'GET',
        url: '/updateSpecialization/' + pk + '/',
        success: function(response){
            $('#name').val(response.name);
            // $('#save_button').attr('data-pk', pk);
            data = response.name
            id=response.pk
            remove_hidden();
            
        },
        error: function(xhr, status, error){
            console.error('Error:', error);
        }
    });
}


///////////////////////////////////Delete specialization

var get_pk
function delete_sp_modalremove(pk) {
    document.getElementById('delete_spec_modal').classList.remove('hidden');
    get_pk=pk
}
function delete_sp_modaladd() {
    document.getElementById('delete_spec_modal').classList.add('hidden');
}
function delete_function(e) {
    e.preventDefault();
    $.ajax({
        type: 'GET',  // Or 'POST' if your Django view expects a POST request
        url: '/deleteSpecialization/' + get_pk + '/',
        success: function(response) {
            console.log(response);
            delete_sp_modaladd(); // Hide the modal
            Specialization_load_table() 
            console.log('Specialization deleted successfully.');
            // location.reload(); // Or remove the row from the table
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
            console.log('An error occurred while trying to delete specialization.');
        }
    });
}
