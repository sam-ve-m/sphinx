Mutatest diagnostic summary
===========================
 - Source location: /home/msa/Projects/prometheus.eagle.python.lionx.com.br/src/projects/sphinx.lionx.com.br/src
 - Test commands: ['python', '-m', 'pytest', '--cov-config=.coveragerc', '--cov=src', 'tests']
 - Mode: s
 - Excluded files: []
 - N locations input: 1000
 - Random seed: None

Random sample details
---------------------
 - Total locations mutated: 86
 - Total locations identified: 86
 - Location sample coverage: 100.00 %


Running time details
--------------------
 - Clean trial 1 run time: 0:00:06.480087
 - Clean trial 2 run time: 0:00:06.208597
 - Mutation trials total run time: 0:12:00.033059

Overall mutation trial summary
==============================
 - ERROR: 2
 - DETECTED: 98
 - SURVIVED: 13
 - TOTAL RUNS: 113
 - RUN DATETIME: 2021-10-01 10:51:01.713636


Mutations by result status
==========================


SURVIVED
--------
 - src/services/builders/suitability/builder.py: (l: 47, c: 19) - mutation from <class '_ast.Gt'> to <class '_ast.GtE'>
 - src/infrastructures/mongo_db/infrastructure.py: (l: 51, c: 22) - mutation from <class '_ast.Gt'> to <class '_ast.NotEq'>
 - src/infrastructures/mongo_db/infrastructure.py: (l: 58, c: 15) - mutation from <class '_ast.And'> to <class '_ast.Or'>
 - src/infrastructures/mongo_db/infrastructure.py: (l: 95, c: 22) - mutation from <class '_ast.Eq'> to <class '_ast.LtE'>
 - src/infrastructures/mongo_db/infrastructure.py: (l: 98, c: 22) - mutation from <class '_ast.Eq'> to <class '_ast.Lt'>
 - src/infrastructures/mongo_db/infrastructure.py: (l: 143, c: 20) - mutation from <class '_ast.Eq'> to <class '_ast.LtE'>
 - src/routers/routes_registers/middleware_functions.py: (l: 30, c: 29) - mutation from <class '_ast.GtE'> to <class '_ast.Gt'>
 - src/repositories/file/repository.py: (l: 200, c: 15) - mutation from <class '_ast.Gt'> to <class '_ast.GtE'>
 - src/services/users/service.py: (l: 83, c: 12) - mutation from <class '_ast.And'> to <class '_ast.Or'>
 - src/services/authentications/service.py: (l: 111, c: 15) - mutation from <class '_ast.NotEq'> to <class '_ast.Lt'>
 - src/services/users/service.py: (l: 127, c: 11) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/services/suitability/service.py: (l: 156, c: 11) - mutation from <class '_ast.NotEq'> to <class '_ast.Gt'>
 - src/services/suitability/service.py: (l: 217, c: 11) - mutation from <class '_ast.NotEq'> to <class '_ast.Lt'>


DETECTED
--------
 - src/services/builders/suitability/builder.py: (l: 20, c: 11) - mutation from <class '_ast.IsNot'> to <class '_ast.Is'>
 - src/services/builders/suitability/builder.py: (l: 47, c: 19) - mutation from <class '_ast.Gt'> to <class '_ast.LtE'>
 - src/services/builders/suitability/builder.py: (l: 47, c: 19) - mutation from <class '_ast.Gt'> to <class '_ast.Lt'>
 - src/services/builders/suitability/builder.py: (l: 47, c: 19) - mutation from <class '_ast.Gt'> to <class '_ast.NotEq'>
 - src/domain/model_decorator/genarate_id.py: (l: 7, c: 7) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/infrastructures/mongo_db/infrastructure.py: (l: 51, c: 22) - mutation from <class '_ast.Gt'> to <class '_ast.Eq'>
 - src/infrastructures/mongo_db/infrastructure.py: (l: 58, c: 27) - mutation from <class '_ast.IsNot'> to <class '_ast.Is'>
 - src/infrastructures/mongo_db/infrastructure.py: (l: 95, c: 11) - mutation from <class '_ast.Or'> to <class '_ast.And'>
 - src/infrastructures/mongo_db/infrastructure.py: (l: 98, c: 11) - mutation from <class '_ast.Or'> to <class '_ast.And'>
 - src/infrastructures/mongo_db/infrastructure.py: (l: 129, c: 11) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/routers/routes_registers/middleware_functions.py: (l: 22, c: 11) - mutation from <class '_ast.And'> to <class '_ast.Or'>
 - src/routers/routes_registers/middleware_functions.py: (l: 30, c: 29) - mutation from <class '_ast.GtE'> to <class '_ast.NotEq'>
 - src/routers/routes_registers/middleware_functions.py: (l: 30, c: 29) - mutation from <class '_ast.GtE'> to <class '_ast.Eq'>
 - src/routers/routes_registers/middleware_functions.py: (l: 30, c: 29) - mutation from <class '_ast.GtE'> to <class '_ast.LtE'>
 - src/routers/routes_registers/middleware_functions.py: (l: 44, c: 11) - mutation from <class '_ast.And'> to <class '_ast.Or'>
 - src/routers/routes_registers/middleware_functions.py: (l: 53, c: 15) - mutation from <class '_ast.In'> to <class '_ast.NotIn'>
 - src/repositories/file/repository.py: (l: 60, c: 11) - mutation from <class '_ast.Or'> to <class '_ast.And'>
 - src/repositories/file/repository.py: (l: 123, c: 11) - mutation from <class '_ast.Or'> to <class '_ast.And'>
 - src/repositories/file/repository.py: (l: 160, c: 11) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/repositories/file/repository.py: (l: 190, c: 11) - mutation from <class '_ast.IsNot'> to <class '_ast.Is'>
 - src/repositories/file/repository.py: (l: 196, c: 11) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/repositories/file/repository.py: (l: 198, c: 15) - mutation from <class '_ast.Eq'> to <class '_ast.Gt'>
 - src/repositories/file/repository.py: (l: 198, c: 15) - mutation from <class '_ast.Eq'> to <class '_ast.GtE'>
 - src/repositories/file/repository.py: (l: 198, c: 15) - mutation from <class '_ast.Eq'> to <class '_ast.Lt'>
 - src/repositories/file/repository.py: (l: 198, c: 15) - mutation from <class '_ast.Eq'> to <class '_ast.NotEq'>
 - src/repositories/file/repository.py: (l: 198, c: 15) - mutation from <class '_ast.Eq'> to <class '_ast.LtE'>
 - src/repositories/file/repository.py: (l: 211, c: 11) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/repositories/file/repository.py: (l: 213, c: 11) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/repositories/file/repository.py: (l: 228, c: 12) - mutation from AugAssign_Add to AugAssign_Div
 - src/repositories/file/repository.py: (l: 228, c: 12) - mutation from AugAssign_Add to AugAssign_Mult
 - src/repositories/file/repository.py: (l: 228, c: 12) - mutation from AugAssign_Add to AugAssign_Sub
 - src/repositories/file/repository.py: (l: 229, c: 11) - mutation from <class '_ast.NotIn'> to <class '_ast.In'>
 - src/repositories/file/repository.py: (l: 235, c: 11) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/repositories/file/repository.py: (l: 235, c: 11) - mutation from <class '_ast.Or'> to <class '_ast.And'>
 - src/repositories/file/repository.py: (l: 235, c: 30) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/repositories/file/repository.py: (l: 250, c: 11) - mutation from <class '_ast.IsNot'> to <class '_ast.Is'>
 - src/services/suitability/service.py: (l: 36, c: 11) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/services/authentications/service.py: (l: 49, c: 11) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/services/users/service.py: (l: 69, c: 11) - mutation from <class '_ast.IsNot'> to <class '_ast.Is'>
 - src/services/authentications/service.py: (l: 69, c: 15) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/services/authentications/service.py: (l: 71, c: 15) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/services/users/service.py: (l: 83, c: 11) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/services/authentications/service.py: (l: 87, c: 11) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/services/authentications/service.py: (l: 93, c: 11) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/services/authentications/service.py: (l: 106, c: 15) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/services/authentications/service.py: (l: 111, c: 15) - mutation from <class '_ast.NotEq'> to <class '_ast.Eq'>
 - src/services/users/service.py: (l: 114, c: 11) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/services/users/service.py: (l: 118, c: 12) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/services/users/service.py: (l: 139, c: 11) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/services/authentications/service.py: (l: 142, c: 11) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/services/users/service.py: (l: 144, c: 11) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/services/suitability/service.py: (l: 153, c: 11) - mutation from <class '_ast.IsNot'> to <class '_ast.Is'>
 - src/services/suitability/service.py: (l: 156, c: 11) - mutation from <class '_ast.NotEq'> to <class '_ast.Eq'>
 - src/services/suitability/service.py: (l: 159, c: 11) - mutation from <class '_ast.IsNot'> to <class '_ast.Is'>
 - src/services/suitability/service.py: (l: 164, c: 11) - mutation from <class '_ast.IsNot'> to <class '_ast.Is'>
 - src/services/suitability/service.py: (l: 174, c: 11) - mutation from <class '_ast.IsNot'> to <class '_ast.Is'>
 - src/services/authentications/service.py: (l: 176, c: 11) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/services/suitability/service.py: (l: 191, c: 11) - mutation from <class '_ast.IsNot'> to <class '_ast.Is'>
 - src/services/suitability/service.py: (l: 214, c: 11) - mutation from <class '_ast.IsNot'> to <class '_ast.Is'>
 - src/services/suitability/service.py: (l: 217, c: 11) - mutation from <class '_ast.NotEq'> to <class '_ast.Eq'>
 - src/services/suitability/service.py: (l: 217, c: 11) - mutation from <class '_ast.NotEq'> to <class '_ast.LtE'>
 - src/services/suitability/service.py: (l: 217, c: 11) - mutation from <class '_ast.NotEq'> to <class '_ast.Gt'>
 - src/services/suitability/service.py: (l: 217, c: 11) - mutation from <class '_ast.NotEq'> to <class '_ast.GtE'>
 - src/services/suitability/service.py: (l: 220, c: 11) - mutation from <class '_ast.IsNot'> to <class '_ast.Is'>
 - src/services/suitability/service.py: (l: 245, c: 11) - mutation from <class '_ast.IsNot'> to <class '_ast.Is'>
 - src/services/users/service.py: (l: 287, c: 11) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/services/users/service.py: (l: 292, c: 11) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/services/users/service.py: (l: 305, c: 11) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/services/users/service.py: (l: 324, c: 11) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/services/users/service.py: (l: 328, c: 11) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/services/users/service.py: (l: 343, c: 11) - mutation from <class '_ast.NotIn'> to <class '_ast.In'>
 - src/services/users/service.py: (l: 346, c: 15) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/services/users/service.py: (l: 364, c: 11) - mutation from <class '_ast.In'> to <class '_ast.NotIn'>
 - src/services/users/service.py: (l: 367, c: 15) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/services/users/service.py: (l: 405, c: 11) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/services/users/service.py: (l: 422, c: 11) - mutation from <class '_ast.IsNot'> to <class '_ast.Is'>
 - src/services/users/service.py: (l: 439, c: 11) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/services/users/service.py: (l: 440, c: 12) - mutation from <class '_ast.And'> to <class '_ast.Or'>
 - src/services/users/service.py: (l: 474, c: 11) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/services/users/service.py: (l: 521, c: 11) - mutation from <class '_ast.IsNot'> to <class '_ast.Is'>
 - src/services/users/service.py: (l: 530, c: 11) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/services/users/service.py: (l: 548, c: 11) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/services/users/service.py: (l: 554, c: 11) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/services/users/service.py: (l: 784, c: 11) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/services/third_part_integration/stone_age.py: (l: 32, c: 15) - mutation from <class '_ast.Eq'> to <class '_ast.NotEq'>
 - src/services/third_part_integration/stone_age.py: (l: 32, c: 15) - mutation from <class '_ast.Eq'> to <class '_ast.GtE'>
 - src/services/third_part_integration/stone_age.py: (l: 32, c: 15) - mutation from <class '_ast.Eq'> to <class '_ast.Gt'>
 - src/services/third_part_integration/stone_age.py: (l: 32, c: 15) - mutation from <class '_ast.Eq'> to <class '_ast.LtE'>
 - src/services/third_part_integration/stone_age.py: (l: 32, c: 15) - mutation from <class '_ast.Eq'> to <class '_ast.Lt'>
 - src/services/third_part_integration/stone_age.py: (l: 32, c: 15) - mutation from <class '_ast.And'> to <class '_ast.Or'>
 - src/services/third_part_integration/stone_age.py: (l: 32, c: 39) - mutation from <class '_ast.In'> to <class '_ast.NotIn'>
 - src/services/third_part_integration/stone_age.py: (l: 32, c: 61) - mutation from <class '_ast.In'> to <class '_ast.NotIn'>
 - src/services/third_part_integration/stone_age.py: (l: 34, c: 17) - mutation from <class '_ast.Eq'> to <class '_ast.NotEq'>
 - src/services/third_part_integration/stone_age.py: (l: 34, c: 17) - mutation from <class '_ast.Eq'> to <class '_ast.LtE'>
 - src/services/third_part_integration/stone_age.py: (l: 34, c: 17) - mutation from <class '_ast.Eq'> to <class '_ast.Lt'>
 - src/services/third_part_integration/stone_age.py: (l: 34, c: 17) - mutation from <class '_ast.Eq'> to <class '_ast.GtE'>
 - src/services/third_part_integration/stone_age.py: (l: 34, c: 17) - mutation from <class '_ast.Eq'> to <class '_ast.Gt'>
 - src/routers/routes_registers/third_part.py: (l: 15, c: 11) - mutation from <class '_ast.And'> to <class '_ast.Or'>


ERROR
-----
 - src/core/abstract_classes/routes_register/register.py: (l: 23, c: 11) - mutation from <class '_ast.Is'> to <class '_ast.IsNot'>
 - src/repositories/file/repository.py: (l: 45, c: 11) - mutation from <class '_ast.NotIn'> to <class '_ast.In'>