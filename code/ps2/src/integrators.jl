export VelocityVerlet
export take_one_step!, take_n_steps!, velocities, positions

abstract type Integrator end
struct VelocityVerlet <: Integrator end

struct StepTracker
    data::Matrix{Particle}
end

apply_periodic_bc(x, L) = x < 0 || x > L ? mod(x, L) : x

function take_one_step!(particles, i, Δt, ::VelocityVerlet)
    L = boxsize(particles)
    particles[i].v += accelerationof(particles, i) * Δt / 2  # 𝐯(t + Δt / 2)
    particles[i].r += particles[i].v * Δt  # 𝐫(t + Δt)
    map!(Base.Fix2(apply_periodic_bc, L), particles[i].r, particles[i].r)
    𝐚 = accelerationof(particles, i)  # 𝐚(t + Δt)
    particles[i].v += 𝐚 * Δt / 2  # 𝐯(t + Δt)
    return particles
end
function take_one_step!(particles, Δt, ::VelocityVerlet)
    for i in eachindex(particles)
        take_one_step!(particles, i, Δt, VelocityVerlet())
    end
    return particles
end

function take_n_steps!(particles, n, Δt, ::VelocityVerlet)
    data = Matrix{Particle}(undef, length(particles), n)
    for i in 1:n
        # Must use `deepcopy`!
        data[:, i] = deepcopy(take_one_step!(particles, Δt, VelocityVerlet()))
    end
    return StepTracker(data)
end

function velocities(tracker::StepTracker)
    return map(tracker.data) do particle
        particle.v
    end
end

function positions(tracker::StepTracker)
    return map(tracker.data) do particle
        particle.r
    end
end
