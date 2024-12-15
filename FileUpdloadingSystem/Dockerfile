FROM public.ecr.aws/j6b7p9b9/tekjava:latest

RUN mkdir -p /etc/dms/crmreporting

WORKDIR /etc/dms/crmreporting

ADD build/libs/*.jar .

CMD java $JAVA_OPTS -Dserver.port=8080 -Dspring.profiles.active=cloud  -jar *.jar

EXPOSE 8080