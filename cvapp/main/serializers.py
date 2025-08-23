from rest_framework import serializers
from .models import CV, Skill, Project

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'link']


class CVSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)

    skill_ids = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(), many=True, write_only=True, required=False
    )
    project_ids = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), many=True, write_only=True, required=False
    )

    class Meta:
        model = CV
        fields = [
            'id', 'firstname', 'lastname', 'role', 'bio', 'contacts',
            'skills', 'projects', 'skill_ids', 'project_ids'
        ]

    def create(self, validated_data):
        skill_objs = validated_data.pop('skill_ids', [])
        project_objs = validated_data.pop('project_ids', [])

        cv = CV.objects.create(**validated_data)
        cv.skills.set(skill_objs)
        cv.projects.set(project_objs)

        return cv

    def update(self, instance, validated_data):
        skill_objs = validated_data.pop('skill_ids', None)
        project_objs = validated_data.pop('project_ids', None)

        instance = super().update(instance, validated_data)

        if skill_objs is not None:
            instance.skills.set(skill_objs)
        if project_objs is not None:
            instance.projects.set(project_objs)

        return instance
