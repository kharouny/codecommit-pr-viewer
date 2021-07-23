FROM debian:10 AS builder

RUN apt-get update
RUN apt-get install -y python3-pip
ADD . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN pip3 install --ignore-installed six

FROM gcr.io/distroless/python3-debian10
COPY --from=builder /app /app
COPY --from=builder /usr/local/lib/python3.7 /usr/local/lib/python3.7

WORKDIR /app
CMD ["/app/bin/pr_aws.py"]
