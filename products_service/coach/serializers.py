from django.core.files.storage import default_storage
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from .models import Coach, CoachInfo, CoachImage

class CoachSimpleSerializer(serializers.ModelSerializer):
    """
        목록 조회용 코치 정보
    """
    name    = serializers.SerializerMethodField()

    class Meta:
        model = Coach
        fields = [
            "uuid",
            "name",
        ]

    def get_name(self, obj):
        return obj.member_name

class CoachCreateSerializer(serializers.ModelSerializer):
    """
        코치 등록용 시리얼라이저
    """
    certification = serializers.FileField(
        error_messages={
            "required": "자격증 파일을 첨부해주세요."
        }
    )
    class Meta:
        model = Coach
        fields = [
            "member_uuid",
            "member_name",
            "member_phone",
            "baseball_career",
            "certification",
        ]

    def file_name(self, certificate):
        type = certificate.content_type
        if type == "application/pdf":
            return "certification.pdf"
        if type == "image/jpeg":
            return f"certification.jpg"
        if type == "image/png":
            return f"certification.png"
        
        raise ValidationError("지원하지 않는 파일 형식입니다.")

    def save(self, **kwargs):
        certificate = self.validated_data.pop("certification")
        coach = Coach.objects.create(**self.validated_data)
        path = f"products/coach/{coach.uuid}/{self.file_name(certificate)}"
        coach.certification.save(path, certificate)

        return coach

class CoachInfoCreateSerializer(serializers.ModelSerializer):
    """
        코치 정보 입력용 시리얼라이저
    """
    class Meta:
        model = CoachInfo
        fields = [
            "intro",
            "regions",
        ]

    def specialty(self, choices):
        if "투구" in choices:
            self.validated_data["pitching"] = True
        if "타격" in choices:
            self.validated_data["batting"] = True
        if "수비" in choices:
            self.validated_data["defense"] = True
        if "포수수비" in choices:
            self.validated_data["catching"] = True
        if "재활" in choices:
            self.validated_data["rehabilitation"] = True
        if "컨디셔닝" in choices:
            self.validated_data["conditioning"] = True

    def level(self, choices):
        if "비기너1" in choices:
            self.validated_data["beginner1"] = True
        if "비기너2" in choices:
            self.validated_data["beginner2"] = True
        if "아마추어" in choices:
            self.validated_data["amateur"] = True
        if "베테랑" in choices:
            self.validated_data["veteran"] = True
        if "루키" in choices:
            self.validated_data["rookie"] = True
        if "엘리트" in choices:
            self.validated_data["elite"] = True

    def lesson_type(self, choices):
        if "개인 레슨" in choices:
            self.validated_data["individual"] = True
        if "소그룹 레슨" in choices:
            self.validated_data["group"] = True
        if "팀 레슨" in choices:
            self.validated_data["team"] = True
        if "기타" in choices:
            self.validated_data["others"] = True

    def upload_images(self, data, uuid):
        images = []
        for image in data:
            # first image: image.obj.cover = True
            cover = False
            if not images:
                cover = True

            path = f"products/coach/{uuid}/{image.name}"
            default_storage.save(path, image)
            coach_image = CoachImage.objects.create(
                coach=self.validated_data["coach"],
                image=path,
                cover=cover
            )
            images.append(coach_image)

        self.validated_data["images"] = images

    def save(self, **kwargs):
        regions = self.validated_data.pop("regions")
        images = self.validated_data.pop("images")
        coach_info = CoachInfo.objects.create(**self.validated_data)
        coach_info.regions.set(regions)
        coach_info.images.set(images)

        return coach_info
