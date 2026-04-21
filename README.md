# Collection Ansible : iTop

Cette collection Ansible fournit des modules et un plugin d'inventaire pour interagir avec iTop (CMDB). Elle permet de gérer des éléments de configuration, d'extraire des informations et d'exécuter des opérations via l'API iTop.

**Namespace / Nom**: `lacrif.itop`

## Contenu

- Modules principaux:
	- `configuration_item` — créer / mettre à jour / supprimer des éléments de configuration
	- `configuration_item_info` — récupérer des informations sur des éléments de configuration
	- `operations` — exécuter des opérations personnalisées via l'API
- Plugin d'inventaire:
	- `itop_inventory` — interroger iTop pour construire dynamiquement un inventaire Ansible
- Utilitaires:
	- `module_utils/api.py` et `module_utils/base.py` — helpers pour l'authentification et les appels API

## Prérequis

- Ansible >= 2.15
- Un serveur iTop accessible et des identifiants API valides

## Installation

Installation depuis Galaxy :

```bash
ansible-galaxy collection install lacrif.itop
```

## Utilisation

Exemples rapides d'utilisation dans un playbook :

- Récupérer des informations sur un élément de configuration :

```yaml
- name: Get configuration item info from iTop
	hosts: localhost
	collections:
		- lacrif.itop
	tasks:
		- name: Fetch CI info
			configuration_item_info:
				name: "Server01"
			register: ci_info

		- debug:
				var: ci_info
```

- Créer ou mettre à jour un élément de configuration :

```yaml
- name: Create or update CI in iTop
	hosts: localhost
	collections:
		- lacrif.itop
	tasks:
		- name: Ensure CI exists
			configuration_item:
				name: "Server01"
				type: "Server"
				attributes:
					description: "Serveur géré par Ansible"
			register: result

		- debug:
				var: result
```

- Utiliser le plugin d'inventaire `itop_inventory` :

Créez un fichier d'inventaire dynamique `itop.yml` ou configurez votre `ansible.cfg` pour utiliser le plugin; se référer à la documentation du plugin dans `plugins/inventory/itop_inventory.py` pour les options attendues.

## Tests d'intégration

Des scénarios d'intégration sont fournis sous le répertoire `tests/integration/targets`. Exécutez les playbooks de test dans un environnement contrôlé pour valider le comportement.
