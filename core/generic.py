from django.core.exceptions import ImproperlyConfigured
from django.views.generic import TemplateView, FormView
from django.http import Http404
from django.conf import settings

db = settings.FIRESTORE_CLIENT

def check_collection(self):
    if not self.collection:
        raise ImproperlyConfigured(
            "%(cls)s is missing a collection. Define "
            "%(cls)s.collection." % {
                'cls': self.__class__.__name__
            }
        )

## Declare a dummy form to confirm deletion
from django import forms
class DeleteConfirmForm(forms.Form):
    def save(self):
        pass

class ListView(TemplateView):
    """Lists all documents from a collection"""
    collection = None

    def get_queryset(self):
        """Return a list of ordered documents from a collection"""
        user_id = self.request.session.get('userid')

        # Get all objects that belongs to user
        query = db.collection(self.collection)\
            .where('owner_id', '==', user_id).get()
        
        # Put all objects as dictionaries in list
        obj_list = list()
        for elem in query:
            obj = elem.to_dict()
            obj['id'] = elem.id
            obj_list.append(obj)
        return obj_list

    def get_context_data(self, **kwargs):
        """Add context variable with the same name of collection"""
        context = super().get_context_data(**kwargs)
        context[self.collection] = self.get_queryset()
        # Confirm delete form
        context['form'] = DeleteConfirmForm(self.request.POST or None)
        return context

class CreateView(FormView):
    """Creates an object on database"""
    collection = None

    def run_database_operation(self, obj):
        ## Add owner_id field
        user_id = self.request.session.get('userid')
        obj['owner_id'] = user_id
        db.collection(self.collection).add(obj)

    def form_valid(self, form):
        """Save data on database if form is valid"""
        check_collection(self)
        self.run_database_operation(form.save())
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.GET.get('next', '/')

class DetailView(TemplateView):
    """Details an objects on database"""
    collection = None

    def get(self, request, id, *args, **kwargs):
        """Save element pk"""
        if id : self.id = id
        else : raise ValueError
        return super().get(request, *args, **kwargs)

    def get_object(self):
        check_collection(self)
        obj = db.collection(self.collection).document(self.id).get()
        if not obj.exists : raise Http404
        else : return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj'] = self.get_object().to_dict()
        return context

class EditView(DetailView, CreateView):
    """Edit an object on database"""
    def post(self, request, id, *args, **kwargs):
        """Save element pk"""
        if id : self.id = id
        else : raise ValueError
        return super().post(request, *args, **kwargs)

    def run_database_operation(self, obj):
        super().get_object().reference.update(obj)

    def get_initial(self):
        return super().get_object().to_dict()

class DeleteView(EditView):
    """Deletes an object using a form for confirmation."""
    form_class = DeleteConfirmForm
    def run_database_operation(self, obj):
        super().get_object().reference.delete()