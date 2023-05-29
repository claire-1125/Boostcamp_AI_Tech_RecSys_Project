
class config():
    seed = 42
    user_dimension = 16
    recipe_dimension = 512
    ingredient_dimension = 512
    hidden_unit = 4
    n_heads = 4

    alpha = 0.1
    drop_out = 0.2
    learning_rate = 1e-2
    weight_decay = 1e-2
    epochs = 50
    batch_size = 128

    load_interaction = False
    device = 'cpu'
    u_idx = 0
    r_idx = ''
    topk = 20
    # parser.add_argument('--seed', type=int, default=42, help='Random seed.')
    # parser.add_argument('--user_dimension', type=int, default=16, help='Random seed.')
    # parser.add_argument('--recipe_dimension', type=int, default=512, help='Random seed.')
    # parser.add_argument('--ingredient_dimension', type=int, default=512, help='Random seed.')
    # parser.add_argument('--hidden_unit', type=int, default=4, help='Random seed.')
    # parser.add_argument('--n_heads', type=int, default=4, help='Random seed.')
    # 
    # parser.add_argument('--alpha', type=float, default=0.1, help='Random seed.')
    # parser.add_argument('--drop_out', type=float, default=0.2, help='Random seed.')
    # parser.add_argument('--learning_rate', type=float, default=1e-2, help='Random seed.')
    # parser.add_argument('--weight_decay', type=float, default=1e-2, help='Random seed.')
    # parser.add_argument('--epochs', type=int, default=50, help='Random seed.')
    # parser.add_argument('--batch_size', type=int, default=128, help='Random seed.')
    # 
    # parser.add_argument('--load_interaction', type=bool, default=True, help='Random seed.')
    # parser.add_argument('--device', type=str, default='cpu', help='Disables CUDA training.')
    # parser.add_argument('--u_idx', type=int, default=0, help='Random seed.') # 없는 index 면 error?
    # parser.add_argument('--r_idx', type=str, default='', help='Random seed.') # _ 로 나뉜거 ?
    # parser.add_argument('--topk', type=int, default=20, help='Random seed.')