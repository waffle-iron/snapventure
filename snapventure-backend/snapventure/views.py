from django.views.generic import DetailView, ListView, UpdateView, CreateView, TemplateView
from .models import Profile, Journey, Inscription, Type, Step, Scan, Edge, State
from django.contrib.auth.models import User
from .forms import ProfileForm, JourneyForm, InscriptionForm, TypeForm, StepForm, ScanForm

# For standard views
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

import qrcode
import base64

# App related views
class Index(TemplateView):
    template_name = "index.html"
    def get(self, request):

        # https://docs.djangoproject.com/en/dev/ref/models/querysets/#first
        # exists

        testU = User.objects.get(username="TestUser1")
        testStep = Step.objects.get(name__contains="Step 3")

        j = Journey.objects.first()
        usrs = User.objects.all()
        steps = Step.objects.filter(journey=j)
        inscriptions = j.inscriptions.all()

        test_scan(testStep, testU.profile)

        return render(request, self.template_name, {'journey' : j, 'users' : usrs, 'inscriptions' : inscriptions, 'steps': steps})


class Scanner(TemplateView):
    template_name = "scan.html"

    def get(self, request, uid):

        # Test prototype of test_scan function
        def test_scan(step, user):

            # Check authentication first :)

            # Check if user started the journey
            if Inscription.objects.filter(journey=step.journey, profile=user).exists():
                if step.root:
                    print("User scanned root step for this journey")
                    Scan(step=step, profile=user, state=State.objects.get(code=800)).save()
                    print("User scanned first code ;)")
                else:
                    # Get parent step of scanned step
                    directParent = Step.objects.get(parent_node__child=step)

                    # Do we have a valid scan for the parent ?
                    if directParent.scan_set.filter(state__code=800, profile=user).exists():
                        print("User scanned parent. Ok.")

                        # User already scanned this code ?
                        if step.scan_set.filter(state__code=800, profile=user).exists():
                            print("User already scanned this step.")
                        else:
                            Scan(step=step, profile=user, state=State.objects.get(code=800)).save()
                            print("Everything ok, add code 800 scan and show related content.")
                    else:
                        print("Previous node note scanned by user. Error.")
                        # Here get last scanned parent and tell user to go
            else:
                print("User must start the journey !")
                Inscription(journey = step.journey, profile=user).save()
                print("User subscribed to journey.")


        # The chosen user for the example
        pro = User.objects.get(username__contains="TestUser6").profile

        # Does the step with that uid exists ?
        if Step.objects.filter(qrcode_uuid=uid).exists():
            print("Looks like the uid is valid")

            # Currently scanned step
            scannedStep = Step.objects.get(qrcode_uuid=uid)

            # Test qrcode generation
            qr = qrcode.QRCode(version=5, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=30)
            qr.add_data("http://localhost:8000/snapventure/scan/" + str(scannedStep.qrcode_uuid))
            qr.make()

            img = qr.make_image()
            img.save("qrcodes/" + str(scannedStep.qrcode_uuid) + ".jpg", "JPEG")

            # Steps from the same journey
            journeySteps = Step.objects.filter(journey=scannedStep.journey)

            # Trigger a scan
            test_scan(scannedStep, pro)

        else:
            print("Invalid step uid.")

        return render(request, self.template_name, {"uid": uid, "journeySteps": journeySteps})


# API related views
class ProfileListView(ListView):
    model = Profile


class ProfileCreateView(CreateView):
    model = Profile
    form_class = ProfileForm


class ProfileDetailView(DetailView):
    model = Profile


class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm


class JourneyListView(ListView):
    model = Journey


class JourneyCreateView(CreateView):
    model = Journey
    form_class = JourneyForm


class JourneyDetailView(DetailView):
    model = Journey


class JourneyUpdateView(UpdateView):
    model = Journey
    form_class = JourneyForm


class InscriptionListView(ListView):
    model = Inscription


class InscriptionCreateView(CreateView):
    model = Inscription
    form_class = InscriptionForm


class InscriptionDetailView(DetailView):
    model = Inscription


class InscriptionUpdateView(UpdateView):
    model = Inscription
    form_class = InscriptionForm


class TypeListView(ListView):
    model = Type


class TypeCreateView(CreateView):
    model = Type
    form_class = TypeForm


class TypeDetailView(DetailView):
    model = Type


class TypeUpdateView(UpdateView):
    model = Type
    form_class = TypeForm


class StepListView(ListView):
    model = Step


class StepCreateView(CreateView):
    model = Step
    form_class = StepForm


class StepDetailView(DetailView):
    model = Step


class StepUpdateView(UpdateView):
    model = Step
    form_class = StepForm


class ScanListView(ListView):
    model = Scan


class ScanCreateView(CreateView):
    model = Scan
    form_class = ScanForm


class ScanDetailView(DetailView):
    model = Scan


class ScanUpdateView(UpdateView):
    model = Scan
    form_class = ScanForm
