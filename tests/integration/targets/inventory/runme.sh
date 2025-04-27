#!/bin/sh

set -eu

# To reduce the amount of warnings coming from the inventory plugins
# enabled by default, we whitelist our plugin only
export ANSIBLE_INVENTORY_ENABLED=community.itop.itop_inventory

# Each inventory source `files/{name}.itop.yml` represents a separate context
# for testing. The tests for each inventory source are in the
# `playbooks/{name}.yml` playbook.

set -x

for inventory_config in files/*.itop.yml
do
  ansible-inventory \
    -i "$inventory_config" \
    --list

  ansible-playbook \
    -i "$inventory_config" \
    "playbooks/$(basename "$inventory_config" .itop.yml).yml"
done
