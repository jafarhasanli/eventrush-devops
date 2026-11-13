#!/bin/bash
set -euxo pipefail

dnf update -y
dnf install -y docker

systemctl enable --now docker

mkdir -p /opt/eventrush

echo "EventRush EC2 bootstrap completed" \
  > /opt/eventrush/bootstrap-status.txt
