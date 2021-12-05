import traceback
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.db import transaction
from wsgiref.util import FileWrapper
from rest_framework import viewsets, serializers, status, generics, views
from rest_framework.decorators import detail_route, list_route, renderer_classes, parser_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, BasePermission
from rest_framework.pagination import PageNumberPagination
from django.urls import reverse
from boranga.components.main.models import Region, District, ApplicationType, Question, GlobalSettings
from boranga.components.main.serializers import RegionSerializer, DistrictSerializer, ApplicationTypeSerializer, QuestionSerializer, GlobalSettingsSerializer
from django.core.exceptions import ValidationError
from django.db.models import Q
from boranga.components.proposals.models import Proposal
from boranga.components.proposals.serializers import ProposalSerializer
from collections import namedtuple
import json
from decimal import Decimal

import logging
logger = logging.getLogger('payment_checkout')


class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = District.objects.all().order_by('id')
    serializer_class = DistrictSerializer

    @detail_route(methods=['GET',])
    def land_parks(self, request, *args, **kwargs):
        instance = self.get_object()
        qs = instance.land_parks
        qs.order_by('id')
        serializer = ParkSerializer(qs,context={'request':request}, many=True)
        return Response(serializer.data)

    @detail_route(methods=['GET',])
    def parks(self, request, *args, **kwargs):
        instance = self.get_object()
        qs = instance.parks
        qs.order_by('id')
        serializer = ParkSerializer(qs,context={'request':request}, many=True)
        return Response(serializer.data)


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Region.objects.all().order_by('id')
    serializer_class = RegionSerializer


class ApplicationTypeViewSet(viewsets.ReadOnlyModelViewSet):
    #queryset = ApplicationType.objects.all().order_by('order')
    queryset = ApplicationType.objects.none()
    serializer_class = ApplicationTypeSerializer

    def get_queryset(self):
        return ApplicationType.objects.order_by('order').filter(visible=True)


class GlobalSettingsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GlobalSettings.objects.all().order_by('id')
    serializer_class = GlobalSettingsSerializer


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


    @list_route(methods=['GET',])
    def tclass_questions_list(self, request, *args, **kwargs):
        qs=Question.objects.filter(application_type__name=ApplicationType.TCLASS)
        serializer = QuestionSerializer(qs,context={'request':request}, many=True)
        return Response(serializer.data)

    @list_route(methods=['GET',])
    def events_questions_list(self, request, *args, **kwargs):
        qs=Question.objects.filter(application_type__name=ApplicationType.EVENT)
        serializer = QuestionSerializer(qs,context={'request':request}, many=True)
        return Response(serializer.data)

