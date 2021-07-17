from django.http import SimpleCookie
from django.template.loader import render_to_string
from django.test import TestCase
from django.test import Client

from blweb.forms import VehicleOptionsForm, VehicleColorOptionsForm
from blweb.models import VehicleMake, VehicleConfig, VehicleColor
from blweb.models import VehicleModel
from blweb.models import VehicleOption

# Test class for unit tests on the vehicle config options
from blweb.views import add_option_price_context_dict, add_color_option_price_context_dict


class TestVehicleConfigOptions(TestCase):
    # set up the environment
    def setUp(self):
        self.client = Client()
        # first create a test make
        self.make = VehicleMake.objects.create(
            name='Ferrari',
            website='www.ferrari.com',
        )
        # now a test model
        self.model = VehicleModel.objects.create(
            name='Roma',
            year=2021,
            make=self.make
        )

        self.option1 = VehicleOption.objects.create(name='Carbon Buckets',
                                                    description='Race-inspired carbon fiber bucket seats',
                                                    price=5000,
                                                    model=self.model)

        self.option2 = VehicleOption.objects.create(name='Shadowline Trim Package',
                                                    description='Enhance the look of your Ferrari with blacked out trim',
                                                    price=4350,
                                                    model=self.model)

        self.paint_color = VehicleColor.objects.create(name='Rosso Corsa',
                                                       description='The original color of Ferrari Racing',
                                                       price=1000,
                                                       model=self.model)

        self.ford = VehicleMake.objects.create(name='Ford',
                                               website='www.ford.com')
        self.mustang = VehicleModel.objects.create(name='Mustang',
                                                   year=2021,
                                                   make=self.ford)
        self.pp1 = VehicleOption.objects.create(name='Performance Pack 1',
                                                description='Mustang Performance Pack 1',
                                                price=3000,
                                                model=self.mustang)

    # test that the page is found
    def test_options_page_exists(self):
        # create a test VehicleConfig from the make above
        veh_config = VehicleConfig.objects.create(make=self.make,
                                                  model=self.model)
        veh_config.save()

        # set the required session variable
        session = self.client.session
        session['vehicle_config'] = veh_config.pk
        session.save()

        response = self.client.get('/vehicle_config_options/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='vehicle_config_options.html')

    def test_options_form(self):
        # create a test VehicleConfig from the make above
        veh_config = VehicleConfig.objects.create(make=self.make,
                                                  model=self.model,
                                                  color=self.paint_color)
        veh_config.save()

        # set the required session variable
        session = self.client.session
        session['vehicle_config'] = veh_config.pk
        session.save()

        form = VehicleOptionsForm(prefix='options',
                                  chosen_model=veh_config.model.pk,
                                  data={'options-options': [self.option1.pk, self.option2.pk]})

        self.assertTrue(form.is_valid())

    def test_colors_form(self):
        # create a test VehicleConfig from the make above
        veh_config = VehicleConfig.objects.create(make=self.make,
                                                  model=self.model,
                                                  color=self.paint_color)
        veh_config.save()

        # set the required session variable
        session = self.client.session
        session['vehicle_config'] = veh_config.pk
        session.save()

        form = VehicleColorOptionsForm(prefix='colors',
                                       chosen_model=veh_config.model.pk,
                                       data={'colors': self.paint_color.pk})

        self.assertTrue(form.is_valid())

    # test the options form field names
    def test_vehicle_options_form_fields(self):
        form = VehicleOptionsForm()
        self.assertIn("options", form.fields)

    # test the colors form field names
    def test_vehicle_color_options_form_fields(self):
        form = VehicleColorOptionsForm()
        self.assertIn("colors", form.fields)

    # test that the price is visible in the rendered form for a color
    def test_vehicle_color_price_rendered(self):
        # create a test VehicleConfig from the make above
        veh_config = VehicleConfig.objects.create(make=self.make,
                                                  model=self.model,
                                                  color=self.paint_color)
        veh_config.save()

        # set the required session variable
        session = self.client.session
        session['vehicle_config'] = veh_config.pk
        session.save()

        context = {'options_form': VehicleOptionsForm(prefix='options', chosen_model=veh_config.model.pk),
                   'colors_form': VehicleColorOptionsForm(prefix='colors', chosen_model=veh_config.model.pk),
                   'veh_make': veh_config.make.name,
                   'veh_model': veh_config.model.name,
                   'veh_model_price': veh_config.model.price}

        context = add_option_price_context_dict(context=context,
                                                veh_config=veh_config)
        context = add_color_option_price_context_dict(context=context,
                                                      veh_config=veh_config)
        html = render_to_string('vehicle_config_options.html', context)
        self.assertIn('Rosso Corsa', html)
        self.assertIn('$1000', html)

    # test that the price is visible in the rendered form for an option
    def test_vehicle_option_price_rendered(self):
        # create a test VehicleConfig from the make above
        veh_config = VehicleConfig.objects.create(make=self.make,
                                                  model=self.model,
                                                  color=self.paint_color)
        veh_config.save()

        # set the required session variable
        session = self.client.session
        session['vehicle_config'] = veh_config.pk
        session.save()

        context = {'options_form': VehicleOptionsForm(prefix='options', chosen_model=veh_config.model.pk),
                   'colors_form': VehicleColorOptionsForm(prefix='colors', chosen_model=veh_config.model.pk),
                   'veh_make': veh_config.make.name,
                   'veh_model': veh_config.model.name,
                   'veh_model_price': veh_config.model.price}

        context = add_option_price_context_dict(context=context,
                                                veh_config=veh_config)
        context = add_color_option_price_context_dict(context=context,
                                                      veh_config=veh_config)
        html = render_to_string('vehicle_config_options.html', context)
        self.assertIn('Carbon Buckets', html)
        self.assertIn('$5000', html)

    # test that the price is visible in the rendered form for a color
    def test_vehicle_color_price_rendered_second(self):
        new_paint_color = VehicleColor.objects.create(name='Grigio Ferro',
                                                      description='Dark grey',
                                                      price=1234,
                                                      model=self.model)

        # create a test VehicleConfig from the make above
        veh_config = VehicleConfig.objects.create(make=self.make,
                                                  model=self.model,
                                                  color=self.paint_color)
        veh_config.save()

        # set the required session variable
        session = self.client.session
        session['vehicle_config'] = veh_config.pk
        session.save()

        context = {'options_form': VehicleOptionsForm(prefix='options', chosen_model=veh_config.model.pk),
                   'colors_form': VehicleColorOptionsForm(prefix='colors', chosen_model=veh_config.model.pk),
                   'veh_make': veh_config.make.name,
                   'veh_model': veh_config.model.name,
                   'veh_model_price': veh_config.model.price}

        context = add_option_price_context_dict(context=context,
                                                veh_config=veh_config)
        context = add_color_option_price_context_dict(context=context,
                                                      veh_config=veh_config)
        html = render_to_string('vehicle_config_options.html', context)
        self.assertIn('Rosso Corsa', html)
        self.assertIn('$1000', html)
        self.assertIn('Grigio Ferro', html)
        self.assertIn('$1234', html)


