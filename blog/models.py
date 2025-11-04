from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


class Category(models.Model):
  name = models.CharField(max_length=60, unique=True)
  slug = models.SlugField(max_length=80, unique=True, blank=True)

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.name)
      super().save(*args, **kwargs)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse("blog.category", args=[self.slug])


class Tag(models.Model):
  name = models.CharField(max_length=40, unique=True)
  slug = models.SlugField(max_length=60, unique=True, blank=True)

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.name)
    super().save(*args, **kwargs)

  def __str__(self):
    return self.name


class Post(models.Model):
  DRAFT = "draft"
  PUBLISHED = "published"
  STATUS_CHOICES = [(DRAFT, "draft"), (PUBLISHED, "published")]

  title = models.CharField(max_length=200)
  slug = models.SlugField(max_length=230, unique=True, blank=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
  category = models.ForeignKey(Category, null=True, blank=True,
                               on_delete=models.SET_NULL)
  tags = models.ManyToManyField(Tag, blank=True)
  cover = models.ImageField(upload_to="covers/", blank=True, null=True)
  excerpt = models.TextField(max_length=300, blank=True)
  content = models.TextField()
  status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=PUBLISHED)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)


  class Meta:
    ordering = ["-created"]

  def save(self, *args, **kwargs):
    if not self.slug:
      base = slugify(self.title)
      slug = base
      i = 1
      while Post.objects.filter(slug=slug).exists():
        i += 1
        slug = f"{base}-{i}"
      self.slug = slug
    super().save(*args, **kwargs)

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse("blog:detail", args=[self.slug])



class Comment(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
  name = models.CharField(max_length=80)
  email = models.EmailField()
  body = models.TextField()
  created = models.DateTimeField(auto_now_add=True)
  active = models.BooleanField(default=True)

  class Meta:
    ordering = ["created"]

    def __str__(self):
      return f"Comment by {self.name} on {self.post}"
