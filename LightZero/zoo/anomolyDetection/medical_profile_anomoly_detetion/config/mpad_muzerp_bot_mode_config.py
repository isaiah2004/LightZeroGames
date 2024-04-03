from easydict import EasyDict
########################################################################
# Description: This file contains the configuration for the bot mode
########################################################################

# ==============================================================
# begin of the most frequently changed config specified by the user
# ==============================================================
collector_env_num = 8
n_episode = 8
evaluator_env_num = 5
num_simulations = 50
update_per_collect = 50
reanalyze_ratio = 0.
batch_size = 256
max_env_step = int(5e5)
# ==============================================================
# end of the most frequently changed config specified by the user
# ==============================================================

mpad_muzero_config = dict(
    exp_name=f'data_mz_ctree/mpad_play-with-bot-mode_seed0',
    env=dict(
        battle_mode='play_with_bot_mode',
        bot_action_type='rule',
        channel_last=False,
        collector_env_num=collector_env_num,
        evaluator_env_num=evaluator_env_num,
        n_evaluator_episode=evaluator_env_num,
        manager=dict(shared_memory=False, ),
    ),
    policy=dict(
        model=dict(
            observation_shape=(3, 6, 7),
            action_space_size=7,
            image_channel=3,
            num_res_blocks=1,
            num_channels=64,
            support_scale=300,
            reward_support_size=601,
            value_support_size=601,
        ),
        cuda=False,
        env_type='board_games',
        action_type='varied_action_space',
        game_segment_length=int(6 * 7 / 2),  # for battle_mode='play_with_bot_mode'
        update_per_collect=update_per_collect,
        batch_size=batch_size,
        optim_type='Adam',
        lr_piecewise_constant_decay=False,
        learning_rate=0.003,
        grad_clip_value=0.5,
        num_simulations=num_simulations,
        reanalyze_ratio=reanalyze_ratio,
        # NOTE：In board_games, we set large td_steps to make sure the value target is the final outcome.
        td_steps=int(6 * 7 / 2),  # for battle_mode='play_with_bot_mode'
        # NOTE：In board_games, we set discount_factor=1.
        discount_factor=1,
        n_episode=n_episode,
        eval_freq=int(2e3),
        replay_buffer_size=int(1e5),
        collector_env_num=collector_env_num,
        evaluator_env_num=evaluator_env_num,
    )
)

mpad_muzero_config = EasyDict(mpad_muzero_config)
main_config = mpad_muzero_config

